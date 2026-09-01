import unittest

from lib.sudoku.grid import Grid
from lib.sudoku.representations import ALPHABETS, decode_grid, encode_grid, verify_round_trip
from tests.test_grid import PUZZLE, SOLUTION


class RepresentationTests(unittest.TestCase):
    def test_all_nine_alphabets_round_trip_puzzles_and_solutions(self) -> None:
        for alphabet in ALPHABETS.values():
            with self.subTest(alphabet=alphabet.name):
                verify_round_trip(Grid.parse(PUZZLE), alphabet)
                verify_round_trip(Grid.parse(SOLUTION), alphabet)

    def test_greek_encoding_matches_declared_bijection(self) -> None:
        encoded = encode_grid(Grid.parse(PUZZLE), ALPHABETS["greek_letters"])
        self.assertEqual(encoded.splitlines()[0], "ε γ . . η . . . .")

    def test_nonce_labels_remain_one_cell_each(self) -> None:
        alphabet = ALPHABETS["nonce_labels"]
        encoded = encode_grid(Grid.parse(SOLUTION), alphabet)
        self.assertEqual(decode_grid(encoded, alphabet), Grid.parse(SOLUTION))
        self.assertEqual(len(encoded.splitlines()[0].split(" ")), 9)

    def test_invalid_symbol_is_rejected(self) -> None:
        encoded = encode_grid(Grid.parse(SOLUTION), ALPHABETS["greek_letters"])
        with self.assertRaisesRegex(ValueError, "invalid symbol"):
            decode_grid(encoded.replace("α", "κ", 1), ALPHABETS["greek_letters"])


if __name__ == "__main__":
    unittest.main()
