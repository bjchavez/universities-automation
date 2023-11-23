from bachelor_degree.pucp_bachelor import faculties_pucp as faculties, thesis_pucp as thesis
from bachelor_degree.pucp_bachelor import thesis_pucp as thesis
from requests.exceptions import HTTPError
from unittest.mock import patch
from bs4 import BeautifulSoup
from typing import assert_type
import unittest
import requests
import urllib3

FACULTIES = "https://repositorio.pucp.edu.pe/index/handle/123456789/7312"


class TestsPucpFaculties(unittest.TestCase):

    def setUp(self):
        urllib3.disable_warnings()

    def test_url(self):
        url = faculties.get_faculties_url()
        self.assertEqual(url, FACULTIES)

    @patch("requests.get")
    def test_response(self, mock_get):
        mock_get.return_value.status_code = 200
        response = faculties.get_faculties_response()
        self.assertEqual(response.status_code, 200)

    @patch("requests.get")
    def test_page(self, mock_get):
        mock_get.return_value.status_code = 400
        req_exception = requests.get(FACULTIES, verify=False)
        self.assertRaises(HTTPError, faculties.get_faculties_page, req_exception)

    def test_faculties(self):
        soup = BeautifulSoup("<body><span class='Z3988'>Faculty AAA</span></body>", "html.parser")
        assert_type(faculties.get_faculties(soup), list[str])


class TestsPucpThesis(unittest.TestCase):

    def setUp(self):
        urllib3.disable_warnings()


if __name__ == "__main__":
    unittest.main()
