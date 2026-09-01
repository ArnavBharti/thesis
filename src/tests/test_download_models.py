import unittest

from lib.config import ModelConfig
from lib.downloads import local_models


class DownloadModelsTests(unittest.TestCase):
    def test_only_enabled_non_api_models_are_downloaded(self) -> None:
        models = (
            ModelConfig(name="local", model_id="org/local", revision="abc"),
            ModelConfig(
                name="api",
                model_id="org/api",
                backend="openai_compatible",
                api_base="https://example.test/v1",
            ),
            ModelConfig(name="disabled", model_id="org/disabled", enabled=False),
        )
        self.assertEqual([model.name for model in local_models(models)], ["local"])

    def test_download_plan_retains_revision(self) -> None:
        model = ModelConfig(name="local", model_id="org/local", revision="deadbeef")
        self.assertEqual(model.revision, "deadbeef")


if __name__ == "__main__":
    unittest.main()
