"""Self-contained writing guidance must preserve evidence and original sections."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "paper/report"))
from build_experiment_guide import HERE, MODELS, STEPS, build_guide, section


class ExperimentGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = build_guide()
        cls.audit = json.loads((HERE / "generated/audit.json").read_text())

    def test_heading_extraction_stops_at_sibling_not_descendant(self):
        sample = "# X\n\n## A\nbody\n### child\nmore\n## B\nother"
        self.assertEqual(section(sample, "## A"), "## A\nbody\n### child\nmore")
        with self.assertRaises(ValueError):
            section(sample, "## missing")

    def test_every_completed_model_step_and_condition_is_local(self):
        for letter, steps in STEPS.items():
            block_heading = next(line for line in self.guide.splitlines()
                                 if line.startswith(f"## {letter}. "))
            block = section(self.guide, block_heading)
            for model, prefix in MODELS.items():
                for step in steps:
                    evidence = self.audit["steps"].get(prefix + "/" + step)
                    if evidence is None:
                        continue
                    self.assertIn(f"#### {model} {step}", block)
                    for condition in evidence["conditions"]:
                        self.assertIn(f"| {condition} |", block)
                    self.assertIn("Full condition-by-difficulty failure", block)
                    self.assertIn("Clues kept / parsed", block)

    def test_completed_qwen_followups_have_verified_evidence(self):
        for step in ("exp6", "exp7", "exp8", "exp9", "exp10"):
            evidence = self.audit["steps"][MODELS["Qwen"] + "/" + step]
            self.assertTrue(evidence["audit"]["complete"])
            self.assertTrue(evidence["audit"]["request_digest_matches"])
            self.assertIn(f"#### Qwen {step}", self.guide)
        self.assertNotIn("No completed Step 12 evidence", self.guide)
        self.assertIn("two regressions", self.guide)
        self.assertIn("Shared-initial revision transitions and compute", self.guide)

    def test_model_specific_labels_and_both_registries_are_included(self):
        self.assertIn("Qwen: exact recorded treatments", self.guide)
        self.assertIn("Completed Qwen token diagnostics", self.guide)
        self.assertIn("Completed GPT-OSS token diagnostics", self.guide)
        self.assertIn("2026-10-03-complete", self.guide)

    def test_original_methods_lenses_and_saved_prompts_are_embedded(self):
        for letter in "ABCDEFGHI":
            heading = next(line for line in self.guide.splitlines() if line.startswith(f"## {letter}. "))
            block = section(self.guide, heading)
            self.assertIn("Exact procedure and implementation details", block)
            self.assertIn("Expanded interpretation", block)
            self.assertIn("Verify this experiment locally", block)
        self.assertIn("user message:", self.guide)
        self.assertIn("Return only a JSON array containing 9 arrays", self.guide)
        self.assertIn("Stage length stops", self.guide)
        self.assertIn("hidden reasoning is not replayed", self.guide.lower())
        narrative = (HERE / "writing_report.md").read_text()
        self.assertEqual(narrative.count("## Lens "), 12)


if __name__ == "__main__":
    unittest.main()
