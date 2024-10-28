# tests/test_utils.py
import unittest
from src.utils import is_even, is_odd, max_in_list, min_in_list

class TestUtils(unittest.TestCase):

    def test_is_even(self):
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(5))

    def test_is_odd(self):
        self.assertTrue(is_odd(5))
        self.assertFalse(is_odd(4))

    def test_max_in_list(self):
        self.assertEqual(max_in_list([1, 3, 5, 7, 9]), 9)
        with self.assertRaises(ValueError):
            max_in_list([])

    def test_min_in_list(self):
        self.assertEqual(min_in_list([1, 3, 5, 7, 9]), 1)
        with self.assertRaises(ValueError):
            min_in_list([])

if __name__ == "__main__":
    unittest.main()

