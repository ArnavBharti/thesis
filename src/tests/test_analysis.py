import unittest

from lib.statistics import _experiment_10, _mcnemar_exact, _wilson_interval, qualification_summary


class AnalysisTests(unittest.TestCase):
    def test_wilson_interval_bounds(self) -> None:
        interval = _wilson_interval(50, 100)
        assert interval is not None
        self.assertLess(interval[0], 0.5)
        self.assertGreater(interval[1], 0.5)

    def test_mcnemar_exact_is_symmetric(self) -> None:
        self.assertEqual(_mcnemar_exact(3, 10), _mcnemar_exact(10, 3))
        self.assertEqual(_mcnemar_exact(0, 0), 1.0)

    def test_qualification_requires_exactly_five_correct(self) -> None:
        values = [
            {
                "request": {"experiment": "qualification"},
                "evaluation": {"outcome": "CORRECT"},
            }
            for _ in range(5)
        ]
        self.assertTrue(qualification_summary(values)["passed"])

    def test_qualification_threshold_can_be_three_for_qwen_screen(self) -> None:
        values = [
            {
                "request": {"experiment": "qualification"},
                "evaluation": {"outcome": "CORRECT" if index < 3 else "INCORRECT"},
            }
            for index in range(5)
        ]
        self.assertFalse(qualification_summary(values)["passed"])
        self.assertTrue(qualification_summary(values, min_correct=3)["passed"])
        values[4]["evaluation"]["outcome"] = "NOT_EVALUATED"
        self.assertFalse(qualification_summary(values, min_correct=3)["passed"])

    def test_revision_totals_exclude_a_reused_initial_call(self) -> None:
        values = [
            {
                "request": {"experiment": "exp10", "condition": "one_pass"},
                "evaluation": {
                    "outcome": "CORRECT",
                    "stages": [
                        {
                            "model_called": False,
                            "evaluation": {"outcome": "CORRECT"},
                            "generation": {
                                "prompt_tokens": 100,
                                "completion_tokens": 20,
                                "latency_seconds": 5.0,
                            },
                        }
                    ],
                },
            }
        ]
        summary = _experiment_10(values)[0]
        self.assertEqual(summary["model_calls"], 0)
        self.assertEqual(summary["total_tokens"], 0)
        self.assertEqual(summary["total_latency_seconds"], 0.0)


if __name__ == "__main__":
    unittest.main()
