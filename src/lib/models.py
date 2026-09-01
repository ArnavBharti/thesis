"""Inference backends for local and OpenAI-compatible models."""

from __future__ import annotations

import importlib.util
import json
import os
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol, Sequence

from .config import InferenceConfig, ModelConfig, RetryConfig
from .records import Generation, Message


class BackendError(RuntimeError):
    """A provider or local inference failure."""


class BackendTimeout(TimeoutError):
    """Inference exceeded the configured request timeout."""


class TokenizerAdapter(Protocol):
    @property
    def identity(self) -> str: ...

    def encode(self, text: str, *, add_special_tokens: bool = False) -> list[int]: ...

    def format_chat(self, messages: Sequence[Message]) -> str: ...


class InferenceBackend(ABC):
    def __init__(self, model: ModelConfig, inference: InferenceConfig, retry: RetryConfig) -> None:
        self.model = model
        self.inference = inference
        self.retry = retry

    @abstractmethod
    def generate(self, messages: Sequence[Message]) -> Generation:
        raise NotImplementedError

    @abstractmethod
    def tokenizer(self) -> TokenizerAdapter:
        raise NotImplementedError

    def close(self) -> None:
        """Release resources held by a backend."""


class HuggingFaceTokenizerAdapter:
    def __init__(self, tokenizer: Any, identity: str) -> None:
        self._tokenizer = tokenizer
        self._identity = identity

    @property
    def identity(self) -> str:
        return self._identity

    def encode(self, text: str, *, add_special_tokens: bool = False) -> list[int]:
        return list(self._tokenizer.encode(text, add_special_tokens=add_special_tokens))

    def format_chat(self, messages: Sequence[Message]) -> str:
        values = [message.to_dict() for message in messages]
        if getattr(self._tokenizer, "chat_template", None):
            return self._tokenizer.apply_chat_template(
                values,
                tokenize=False,
                add_generation_prompt=True,
            )
        return "\n\n".join(f"{message.role.upper()}: {message.content}" for message in messages) + "\n\nASSISTANT:"


def load_huggingface_tokenizer(model: ModelConfig) -> HuggingFaceTokenizerAdapter:
    try:
        from transformers import AutoTokenizer
    except ImportError as error:  # pragma: no cover - optional inference dependency
        raise BackendError("transformers is required to load a local tokenizer") from error
    tokenizer = AutoTokenizer.from_pretrained(
        model.resolved_tokenizer_id,
        revision=model.revision,
        trust_remote_code=model.trust_remote_code,
        local_files_only=model.local_files_only,
    )
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    return HuggingFaceTokenizerAdapter(tokenizer, model.resolved_tokenizer_id)


class TransformersBackend(InferenceBackend):
    def __init__(self, model: ModelConfig, inference: InferenceConfig, retry: RetryConfig) -> None:
        super().__init__(model, inference, retry)
        try:
            import torch
            from transformers import AutoModelForCausalLM
        except ImportError as error:  # pragma: no cover - optional inference dependency
            raise BackendError("the transformers backend requires torch and transformers") from error

        self._torch = torch
        self._tokenizer_adapter = load_huggingface_tokenizer(model)
        tokenizer = self._tokenizer_adapter._tokenizer
        load_arguments: dict[str, Any] = {
            "revision": model.revision,
            "trust_remote_code": model.trust_remote_code,
            "local_files_only": model.local_files_only,
            "device_map": "auto",
        }
        if model.dtype != "auto":
            dtype = getattr(torch, model.dtype, None)
            if dtype is None:
                raise BackendError(f"unknown torch dtype {model.dtype!r}")
            load_arguments["torch_dtype"] = dtype
        self._model = AutoModelForCausalLM.from_pretrained(model.resolved_model_id, **load_arguments)
        self._model.eval()
        self._tokenizer = tokenizer

    def tokenizer(self) -> TokenizerAdapter:
        return self._tokenizer_adapter

    def generate(self, messages: Sequence[Message]) -> Generation:
        started = time.monotonic()
        prompt = self._tokenizer_adapter.format_chat(messages)
        inputs = self._tokenizer(prompt, return_tensors="pt")
        device = next(self._model.parameters()).device
        inputs = {name: value.to(device) for name, value in inputs.items()}
        do_sample = self.inference.temperature > 0
        arguments: dict[str, Any] = {
            **inputs,
            "max_new_tokens": self.inference.max_new_tokens,
            "do_sample": do_sample,
            "pad_token_id": self._tokenizer.pad_token_id,
        }
        if do_sample:
            arguments["temperature"] = self.inference.temperature
            arguments["top_p"] = self.inference.top_p
            generator = self._torch.Generator(device=device)
            generator.manual_seed(self.inference.seed)
            arguments["generator"] = generator
        with self._torch.inference_mode():
            output = self._model.generate(**arguments)
        prompt_length = inputs["input_ids"].shape[-1]
        generated = output[0, prompt_length:]
        text = self._tokenizer.decode(generated, skip_special_tokens=True)
        return Generation(
            text=text,
            finish_reason="length" if generated.shape[-1] >= self.inference.max_new_tokens else "stop",
            prompt_tokens=prompt_length,
            completion_tokens=generated.shape[-1],
            latency_seconds=time.monotonic() - started,
            provider_metadata={"backend": "transformers"},
        )


class VLLMBackend(InferenceBackend):
    def __init__(self, model: ModelConfig, inference: InferenceConfig, retry: RetryConfig) -> None:
        super().__init__(model, inference, retry)
        try:
            from vllm import LLM
        except ImportError as error:  # pragma: no cover - optional inference dependency
            raise BackendError("the vLLM backend requires vllm") from error
        self._tokenizer_adapter = load_huggingface_tokenizer(model)
        model_location = _local_snapshot_path(model) if model.local_files_only else model.resolved_model_id
        tokenizer_location = (
            model_location
            if model.resolved_tokenizer_id == model.resolved_model_id
            else model.resolved_tokenizer_id
        )
        arguments: dict[str, Any] = {
            "model": model_location,
            "tokenizer": tokenizer_location,
            "dtype": model.dtype,
            "tensor_parallel_size": model.tensor_parallel_size,
            "trust_remote_code": model.trust_remote_code,
        }
        if model.revision and model_location == model.resolved_model_id:
            arguments["revision"] = model.revision
        arguments.update(model.extra.get("vllm", {}))
        self._llm = LLM(**arguments)

    def tokenizer(self) -> TokenizerAdapter:
        return self._tokenizer_adapter

    def generate(self, messages: Sequence[Message]) -> Generation:
        try:
            from vllm import SamplingParams
        except ImportError as error:  # pragma: no cover
            raise BackendError("the vLLM backend requires vllm") from error
        started = time.monotonic()
        prompt = self._tokenizer_adapter.format_chat(messages)
        parameters = SamplingParams(
            max_tokens=self.inference.max_new_tokens,
            temperature=self.inference.temperature,
            top_p=self.inference.top_p,
            seed=self.inference.seed,
        )
        result = self._llm.generate([prompt], parameters, use_tqdm=False)[0]
        candidate = result.outputs[0]
        prompt_token_ids = getattr(result, "prompt_token_ids", None)
        completion_token_ids = getattr(candidate, "token_ids", None)
        return Generation(
            text=candidate.text,
            finish_reason=str(getattr(candidate, "finish_reason", "stop")),
            prompt_tokens=len(prompt_token_ids) if prompt_token_ids is not None else None,
            completion_tokens=len(completion_token_ids) if completion_token_ids is not None else None,
            latency_seconds=time.monotonic() - started,
            provider_metadata={"backend": "vllm"},
        )


class OpenAICompatibleBackend(InferenceBackend):
    def __init__(self, model: ModelConfig, inference: InferenceConfig, retry: RetryConfig) -> None:
        super().__init__(model, inference, retry)
        self._tokenizer_adapter: TokenizerAdapter | None = None
        if model.tokenizer_id:
            self._tokenizer_adapter = load_huggingface_tokenizer(model)

    def tokenizer(self) -> TokenizerAdapter:
        if self._tokenizer_adapter is None:
            raise BackendError(
                f"model {self.model.name} requires tokenizer_id for local token diagnostics"
            )
        return self._tokenizer_adapter

    def generate(self, messages: Sequence[Message]) -> Generation:
        assert self.model.api_base is not None
        url = self.model.api_base.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model.model_id,
            "messages": [message.to_dict() for message in messages],
            "max_completion_tokens": self.inference.max_new_tokens,
            "temperature": self.inference.temperature,
            "top_p": self.inference.top_p,
            "seed": self.inference.seed,
        }
        for parameter in self.model.extra.get("omit_parameters", []):
            payload.pop(parameter, None)
        payload.update(self.model.extra.get("request", {}))
        headers = {"Content-Type": "application/json", "X-OpenRouter-Metadata": "enabled"}
        headers.update(self.model.extra.get("headers", {}))
        if self.model.api_key_env:
            key = os.environ.get(self.model.api_key_env)
            if not key:
                raise BackendError(f"missing API key environment variable {self.model.api_key_env}")
            headers["Authorization"] = f"Bearer {key}"
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=self.retry.timeout_seconds) as response:
                value = json.loads(response.read().decode("utf-8"))
        except TimeoutError as error:
            raise BackendTimeout(str(error)) from error
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise BackendError(f"HTTP {error.code}: {body[:1000]}") from error
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, IndexError, TypeError) as error:
            raise BackendError(str(error)) from error
        choice = value["choices"][0]
        usage = value.get("usage", {})
        required_provider = self.model.extra.get("protocol", {}).get("required_provider")
        actual_provider = value.get("provider")
        if required_provider and actual_provider and actual_provider != required_provider:
            raise BackendError(
                f"provider routing violation: expected {required_provider}, received {actual_provider}"
            )
        return Generation(
            text=choice["message"]["content"] or "",
            finish_reason=choice.get("finish_reason"),
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            latency_seconds=time.monotonic() - started,
            provider_metadata={
                "backend": "openai_compatible",
                "response_id": value.get("id"),
                "routed_model": value.get("model"),
                "provider": value.get("provider"),
                "created": value.get("created"),
                "system_fingerprint": value.get("system_fingerprint"),
                "usage": usage,
                "openrouter_metadata": value.get("openrouter_metadata"),
            },
        )


class StaticBackend(InferenceBackend):
    """Dependency-free deterministic backend for dry runs and tests."""

    def __init__(self, model: ModelConfig, inference: InferenceConfig, retry: RetryConfig) -> None:
        super().__init__(model, inference, retry)
        self.responses = list(model.extra.get("responses", []))
        self.default_response = model.extra.get("response", "")
        self.calls = 0

    def tokenizer(self) -> TokenizerAdapter:
        return CharacterTokenizer()

    def generate(self, messages: Sequence[Message]) -> Generation:
        del messages
        started = time.monotonic()
        if self.calls < len(self.responses):
            text = self.responses[self.calls]
        else:
            text = self.default_response
        self.calls += 1
        return Generation(
            text=text,
            finish_reason="stop",
            prompt_tokens=None,
            completion_tokens=None,
            latency_seconds=time.monotonic() - started,
            provider_metadata={"backend": "static"},
        )


class CharacterTokenizer:
    @property
    def identity(self) -> str:
        return "character-tokenizer-v1"

    def encode(self, text: str, *, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [ord(character) for character in text]

    def format_chat(self, messages: Sequence[Message]) -> str:
        return "\n".join(f"{message.role}: {message.content}" for message in messages)


def build_backend(
    model: ModelConfig,
    inference: InferenceConfig,
    retry: RetryConfig,
) -> InferenceBackend:
    backend = model.backend
    if backend == "auto":
        backend = "vllm" if importlib.util.find_spec("vllm") is not None else "transformers"
    if backend == "vllm":
        return VLLMBackend(model, inference, retry)
    if backend == "transformers":
        return TransformersBackend(model, inference, retry)
    if backend == "openai_compatible":
        return OpenAICompatibleBackend(model, inference, retry)
    if backend == "static":
        return StaticBackend(model, inference, retry)
    raise BackendError(f"unsupported backend {backend!r}")


def probe_model(model: ModelConfig) -> tuple[bool, str]:
    if model.backend == "static":
        return True, "dependency-free static test backend"
    if model.backend == "openai_compatible":
        if model.api_key_env and not os.environ.get(model.api_key_env):
            return False, f"missing API key environment variable {model.api_key_env}"
        return True, "configured remote or local OpenAI-compatible endpoint"
    model_path = Path(model.resolved_model_id)
    if model_path.exists():
        return True, f"local path exists: {model_path}"
    if importlib.util.find_spec("transformers") is None:
        return False, "transformers is not installed and model_id is not a local path"
    try:
        from transformers import AutoConfig

        AutoConfig.from_pretrained(
            model.resolved_model_id,
            revision=model.revision,
            trust_remote_code=model.trust_remote_code,
            local_files_only=True,
        )
        return True, "model configuration found in the local Hugging Face cache"
    except Exception as error:  # transformers raises several cache/config-specific types
        return False, f"model is not available locally: {error}"


def _local_snapshot_path(model: ModelConfig) -> str:
    direct_path = Path(model.resolved_model_id)
    if direct_path.exists():
        return str(direct_path.resolve())
    try:
        from huggingface_hub import snapshot_download
    except ImportError as error:  # pragma: no cover - optional inference dependency
        raise BackendError("huggingface-hub is required to resolve a cached model snapshot") from error
    try:
        return snapshot_download(
            repo_id=model.resolved_model_id,
            revision=model.revision,
            local_files_only=True,
        )
    except Exception as error:
        raise BackendError(
            f"pinned model snapshot is missing for {model.name}; run download_models.py first"
        ) from error
