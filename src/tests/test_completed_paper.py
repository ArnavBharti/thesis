"""Completed-paper artifacts must derive from the preserved two-model evidence."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "paper/report"))
from analyze_evidence import read_rows
from lib import statistics

SNAPSHOT = ROOT / "evidence/snapshots/2026-10-03-complete"
MODELS = {"GPT-OSS": "local-models-v1/gpt-oss-120b-local",
          "Qwen": "qwen-3.8-27b-v2/qwen-3.8-27b-local"}


class CompletedPaperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {}
        for name, prefix in MODELS.items():
            directory = SNAPSHOT / "experiment_outputs" / prefix
            cls.rows[name] = [row for path in sorted(directory.glob("*/shard-*.jsonl.gz"))
                              for row in read_rows(path)]

    def test_both_server_analyses_reproduce_from_saved_rows(self):
        for model, prefix in MODELS.items():
            rows = self.rows[model]
            server = json.loads((SNAPSHOT / "experiment_outputs" / prefix / "analysis/summary.json").read_text())
            self.assertEqual(server["record_count"], len(rows))
            for field, function in (
                ("groups", statistics._group_summaries),
                ("failure_labels", statistics._failure_labels),
                ("pilot", statistics.pilot_summary),
                ("experiment_5", statistics._experiment_5),
                ("experiment_7_regression", statistics._experiment_7),
                ("experiment_10", statistics._experiment_10),
            ):
                self.assertEqual(server[field], function(rows), (model, field))

    def test_reused_mechanism_generations_match_original_main(self):
        for model, rows in self.rows.items():
            originals = {r["request"]["request_id"]: r for r in rows if r["request"]["experiment"] == "exp4"}
            count = 0
            for row in rows:
                if row["request"]["experiment"] not in {"exp6", "exp8"}:
                    continue
                generation = row["generation"]
                original_id = generation["provider_metadata"].get("reused_from_request_id")
                if original_id:
                    count += 1
                    comparable = dict(generation)
                    comparable["provider_metadata"] = dict(generation["provider_metadata"])
                    comparable["provider_metadata"].pop("reused_from_request_id")
                    self.assertEqual(comparable, originals[original_id]["generation"], model)
            self.assertEqual(count, 75)

    def test_qwen_identical_prompt_binary_agreement_is_observed(self):
        conditions = ("rules_fully_explicit", "mapping_alphabet_only", "output_spaced", "empty_dot")
        groups = {c: {r["request"]["puzzle_id"]: r for r in self.rows["Qwen"]
                      if r["request"]["experiment"] == "exp9" and r["request"]["condition"] == c}
                  for c in conditions}
        baseline = groups[conditions[0]]
        self.assertEqual(len(baseline), 9)
        for group in groups.values():
            for puzzle_id, row in group.items():
                self.assertEqual(row["request"]["messages"], baseline[puzzle_id]["request"]["messages"])
                self.assertEqual(row["evaluation"]["outcome"] == "CORRECT",
                                 baseline[puzzle_id]["evaluation"]["outcome"] == "CORRECT")

    def test_both_registries_have_full_symbol_and_prompt_scope(self):
        for prefix in MODELS.values():
            rows = read_rows(SNAPSHOT / "experiment_outputs" / prefix / "exp3/representation-registry.jsonl.gz")
            self.assertEqual(sum(r["kind"] == "symbol" for r in rows), 81)
            self.assertEqual(sum(r["kind"] == "prompt" for r in rows), 2700)
            self.assertEqual(len(rows), 2781)


if __name__ == "__main__":
    unittest.main()
