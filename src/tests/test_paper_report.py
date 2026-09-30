"""Offline reporting invariants, independent of inference and server access."""

import copy
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "paper/report"))
from analyze_evidence import audit_step, category, cross_model, grid_diagnostics, paired_retention, summarize
from lib.evaluation import evaluate_generation
from lib.records import ExperimentRequest, Generation, Message, shard_for
from lib.sudoku.grid import Grid
from tests.test_grid import PUZZLE, SOLUTION


def row(text=None, finish="stop", condition="arabic_digits", puzzle_id="T001"):
    request = ExperimentRequest(
        experiment="report-test", condition=condition, model="mock",
        messages=(Message("user", "solve"),), puzzle_id=puzzle_id,
        puzzle=Grid.parse(PUZZLE).compact, expected_solution=Grid.parse(SOLUTION).compact,
        metadata={"evaluation_kind": "sudoku", "output_symbols": list("123456789"), "difficulty": "easy"},
    )
    generation = Generation(text if text is not None else SOLUTION.strip(), finish, 10, 81, 2.0)
    return {"request": request.to_dict(), "generation": asdict(generation),
        "status": "OK", "evaluation": evaluate_generation(request, generation)}


class PaperReportTests(unittest.TestCase):
    def test_categories_are_exclusive_and_prioritized(self):
        correct = row(finish="length")
        # A complete correct grid remains correct even if the finish reason
        # is length. Length stops are a failure category only when incorrect.
        self.assertEqual(category(correct), "correct")
        incorrect = row("unfinished", finish="length")
        self.assertEqual(category(incorrect), "truncated")
        incorrect["status"] = "TIMEOUT"
        self.assertEqual(category(incorrect), "operational_error")
        self.assertEqual(category(row("unparseable")), "other_output_error")

    def test_independent_checker_validates_solution(self):
        check = grid_diagnostics(row())
        self.assertTrue(check["parseable"])
        self.assertTrue(check["clues_preserved"])
        self.assertTrue(check["sudoku_valid"])
        self.assertTrue(check["solution_equal"])

    def test_valid_units_do_not_imply_preserved_clues(self):
        swapped = SOLUTION.translate(str.maketrans("12", "21"))
        check = grid_diagnostics(row(swapped))
        self.assertTrue(check["sudoku_valid"])
        self.assertFalse(check["clues_preserved"])
        self.assertGreater(check["changed_clues"], 0)
        self.assertEqual(category(row(swapped)), "incorrect_grid")

    def test_unparseable_is_not_counted_as_preserved(self):
        summary = summarize([row(), row("no grid")])
        self.assertEqual(summary["sudoku_requests"], 2)
        self.assertEqual(summary["parseable"], 1)
        self.assertEqual(summary["clues_preserved"], 1)

    def test_extra_spaces_fail_strict_grid_parsing(self):
        self.assertFalse(grid_diagnostics(row(SOLUTION.replace(" ", "  ")))["parseable"])

    def test_paired_retention_records_gains_as_well_as_losses(self):
        rows = [row(puzzle_id="A"), row("bad", "stop", "greek_letters", "A"),
                row("bad", puzzle_id="B"), row(condition="greek_letters", puzzle_id="B")]
        paired = paired_retention(rows)[0]
        self.assertEqual((paired["paired_n"], paired["baseline_only"], paired["condition_only"]), (2, 1, 1))
        self.assertEqual(paired["retained"], 0)
        self.assertEqual(paired["mcnemar_p"], 1.0)

    def test_partial_cross_model_does_not_bootstrap(self):
        result = cross_model([row(), row("bad", puzzle_id="B")], [row(), row(puzzle_id="B")])
        self.assertEqual(result["both_correct"], 1)
        self.assertEqual(result["qwen_only"], 1)
        self.assertNotIn("stratified_puzzle_bootstrap_95_pp", result)

    def test_complete_bootstrap_preserves_whole_puzzle_effects(self):
        models = [[], []]
        for tier in ("easy", "medium", "hard"):
            for puzzle in range(20):
                for alphabet in range(9):
                    for index, outcome in enumerate(("INCORRECT", "CORRECT")):
                        models[index].append({"request": {
                            "puzzle_id": f"{tier}-{puzzle}", "condition": str(alphabet),
                            "metadata": {"difficulty": tier}}, "evaluation": {"outcome": outcome}})
        result = cross_model(*models)
        self.assertEqual(result["paired_requests"], 540)
        self.assertEqual(result["qwen_minus_gpt_pp"], 100.0)
        self.assertEqual(result["stratified_puzzle_bootstrap_95_pp"], [100.0, 100.0])
        self.assertEqual(result["bootstrap_replicates"], 10000)

    def write_step(self, directory, value, marker=True):
        path = directory / "shard-000-of-001.jsonl"
        path.write_text(json.dumps(value) + "\n")
        request_id = value["request"]["request_id"]
        (directory / "request-manifest.json").write_text(json.dumps({
            "request_count": 1, "request_id_sha256": hashlib.sha256(request_id.encode()).hexdigest()}))
        if marker:
            (directory / "part-001-of-001.complete.json").write_text(json.dumps({
                "part": 1, "parts": 1, "status": "COMPLETE", "eligible_requests": 1}))
        return path

    def test_completion_requires_marker_digest_and_content_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            value = row()
            path = self.write_step(directory, value, marker=False)
            self.assertFalse(audit_step(directory, [value], [path])["complete"])
            self.write_step(directory, value)
            self.assertTrue(audit_step(directory, [value], [path])["complete"])
            value["request"]["messages"][0]["content"] = "changed prompt"
            path.write_text(json.dumps(value) + "\n")
            result = audit_step(directory, [value], [path])
            self.assertFalse(result["complete"])
            self.assertTrue(any("content hash mismatch" in error for error in result["errors"]))

    def test_duplicate_ids_block_completion(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            value = row()
            path = self.write_step(directory, value)
            result = audit_step(directory, [value, copy.deepcopy(value)], [path])
            self.assertIn("duplicate request IDs", result["errors"])
            self.assertFalse(result["complete"])

    def test_wrong_hash_shard_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            value = row()
            index = 1 - shard_for(value["request"]["request_id"], 2)
            path = directory / f"shard-{index:03d}-of-002.jsonl"
            path.write_text(json.dumps(value) + "\n")
            result = audit_step(directory, [value], [path])
            self.assertTrue(any("wrong hash shard" in error for error in result["errors"]))

    def test_backup_round_trip_checksums_and_secret_exclusion(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source, destination = base / "source", base / "backup"
            (source / "experiment_outputs").mkdir(parents=True)
            raw = b'{"final":"exact preserved bytes"}\n'
            (source / "experiment_outputs/result.jsonl").write_bytes(raw)
            (source / "experiment_outputs/.env").write_text("DO_NOT_COPY")
            command = [sys.executable, str(ROOT / "paper/report/prepare_snapshot.py"), str(source), str(destination)]
            subprocess.run(command, check=True, capture_output=True)
            manifest = json.loads((destination / "snapshot-manifest.json").read_text())
            self.assertEqual(len(manifest["files"]), 1)
            archive = destination / "experiment_outputs/result.jsonl.gz"
            first = archive.read_bytes()
            self.assertEqual(gzip.decompress(first), raw)
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(archive.read_bytes(), first)
            subprocess.run(command + ["--verify"], check=True, capture_output=True)
            archive.write_bytes(gzip.compress(b"changed"))
            failed = subprocess.run(command + ["--verify"], capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn(b"checksum mismatch", failed.stderr)


if __name__ == "__main__":
    unittest.main()
