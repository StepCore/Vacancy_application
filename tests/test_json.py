import json
import unittest
from unittest.mock import mock_open, patch

from src.api_settings import FileSaverToJSON


class TestFileSaverToJSON(unittest.TestCase):

    def setUp(self):
        self.file_path = "./data/vacancies.json"
        self.file_saver = FileSaverToJSON(self.file_path)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"title": "Vacancy 1"}, {"title": "Vacancy 2"}]),
    )
    def test_load_success(self, mock_file):
        result = self.file_saver.load()
        self.assertEqual(result, [{"title": "Vacancy 1"}, {"title": "Vacancy 2"}])
        mock_file.assert_called_once_with(self.file_path, "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_file_not_found(self, mock_file):
        result = self.file_saver.load()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with(self.file_path, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_json_decode_error(self, mock_file):
        result = self.file_saver.load()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with(self.file_path, "r", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
