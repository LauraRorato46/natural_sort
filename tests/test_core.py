import unittest

from natural_sort.core import natural_sort_key, natural_sorted


class TestNaturalSortKey(unittest.TestCase):
    def test_numeric_substrings_ordered_by_value(self):
        self.assertLess(
            natural_sort_key("file2.txt"),
            natural_sort_key("file10.txt"),
        )

    def test_non_numeric_substrings_ordered_lexicographically(self):
        self.assertLess(
            natural_sort_key("apple"),
            natural_sort_key("banana"),
        )

    def test_leading_zeros_do_not_affect_value(self):
        # The numeric value is what matters, so file7 and file007 compare equal
        # on their numeric chunk. The surrounding text is also equal, so the
        # keys are fully equal.
        self.assertEqual(
            natural_sort_key("file7"),
            natural_sort_key("file007"),
        )

    def test_non_str_input_is_stringified(self):
        self.assertLess(
            natural_sort_key(2),
            natural_sort_key(10),
        )

    def test_key_is_a_tuple(self):
        self.assertIsInstance(natural_sort_key("abc123"), tuple)


class TestNaturalSorted(unittest.TestCase):
    def test_sorts_file_list_as_expected(self):
        names = ["file10.txt", "file2.txt", "file1.txt"]
        self.assertEqual(
            natural_sorted(names),
            ["file1.txt", "file2.txt", "file10.txt"],
        )

    def test_with_key_function(self):
        # Sort dicts by a field that contains numbers.
        rows = [{"n": "item10"}, {"n": "item2"}, {"n": "item1"}]
        result = natural_sorted(rows, key=lambda r: r["n"])
        self.assertEqual([r["n"] for r in result], ["item1", "item2", "item10"])

    def test_reverse(self):
        names = ["file1", "file2", "file10"]
        self.assertEqual(
            natural_sorted(names, reverse=True),
            ["file10", "file2", "file1"],
        )

    def test_mixed_numbers_and_text(self):
        items = ["1a", "1b", "2a", "10a", "1"]
        self.assertEqual(
            natural_sorted(items),
            ["1", "1a", "1b", "2a", "10a"],
        )

    def test_returns_a_list(self):
        self.assertIsInstance(natural_sorted(["b", "a"]), list)

    def test_no_numbers_just_lexicographic(self):
        items = ["banana", "apple", "cherry"]
        self.assertEqual(natural_sorted(items), ["apple", "banana", "cherry"])

    def test_numbers_only(self):
        items = ["100", "2", "10", "1"]
        self.assertEqual(natural_sorted(items), ["1", "2", "10", "100"])


if __name__ == "__main__":
    unittest.main()
