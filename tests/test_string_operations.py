# tests/test_string_operations.py
import unittest
from src.string_operations import concatenate, to_uppercase, to_lowercase, split_string

class TestStringOperations(unittest.TestCase):

    def test_concatenate(self):
        self.assertEqual(concatenate("Hello", "World"), "HelloWorld")

    def test_to_uppercase(self):
        self.assertEqual(to_uppercase("hello"), "HELLO")

    def test_to_lowercase(self):
        self.assertEqual(to_lowercase("HELLO"), "hello")

    def test_split_string(self):
        self.assertEqual(split_string("hello world"), ["hello", "world"])
        self.assertEqual(split_string("one,two,three", ","), ["one", "two", "three"])

if __name__ == "__main__":
    unittest.main()

