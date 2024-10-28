import unittest
from src.utils import read_json_file


class TestUtils(unittest.TestCase):
    def test_read_json_file(self):
        result = read_json_file("data/operations.json")
        self.assertIsInstance(result, list)

    def test_empty_file(self):
        with open("data/empty.json", "w") as f:
            f.write("")
        result = read_json_file("data/empty.json")
        self.assertEqual(result, [])

    def test_non_existent_file(self):
        result = read_json_file("data/non_existent.json")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
