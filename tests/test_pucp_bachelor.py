from bachelor_degree.pucp_bachelor import faculties_pucp
from bachelor_degree.pucp_bachelor import thesis_pucp
from requests.exceptions import HTTPError
from unittest.mock import patch
from bs4 import BeautifulSoup
from collections import deque
import unittest
import requests
import urllib3


class TestsPucpFaculties(unittest.TestCase):

    def setUp(self):
        urllib3.disable_warnings()
        self.faculties_url = "https://repositorio.pucp.edu.pe/index/handle/123456789/7312"

    def test_url(self):
        url = faculties_pucp.get_faculties_url()
        self.assertEqual(url, self.faculties_url)
        self.assertIsInstance(url, str)

    @patch("requests.get")
    def test_response(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertEqual(faculties_pucp.get_faculties_response().status_code, 200)

    @patch("requests.get")
    def test_page(self, mock_get):
        mock_get.return_value.status_code = 400
        req_exception = requests.get(self.faculties_url, verify=False)
        self.assertRaises(HTTPError, faculties_pucp.get_faculties_page, req_exception)

    def test_faculties(self):
        soup = BeautifulSoup("<body><span class='Z3988'>Faculty AAA</span></body>", "html.parser")
        self.assertIsInstance(faculties_pucp.get_faculties(soup), list)


class TestsPucpThesis(unittest.TestCase):

    def setUp(self):
        urllib3.disable_warnings()
        self.thesis_url = "https://repositorio.pucp.edu.pe/index/handle/123456789"
        self.thesis_ids = [9117, 170514, 9118, 129392,
                           135248, 9119, 9120, 9121,
                           9122, 9123, 9124, 9125, 129361]

    def test_url(self):
        url = thesis_pucp.get_thesis_url()
        self.assertEqual(url, self.thesis_url)

    def test_ids(self):
        ids = thesis_pucp.get_thesis_ids()
        self.assertEqual(ids, self.thesis_ids)

    @patch.object(thesis_pucp, "get_thesis_response")
    def test_responses(self, mock_responses):
        mock_responses.return_value = deque([200, 200, 200, 200,
                                             200, 200, 200, 200,
                                             200, 200, 200, 200, 200])
        self.assertEqual(len(thesis_pucp.get_thesis_response()), 13)
        self.assertIsInstance(thesis_pucp.get_thesis_response(), deque)


if __name__ == "__main__":
    unittest.main()
