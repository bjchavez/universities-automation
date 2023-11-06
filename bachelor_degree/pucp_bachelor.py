from importlib import import_module
from bs4 import BeautifulSoup
from collections import deque
import requests


class PucpFaculties:
    def __init__(self, faculties_url):
        self.faculties_url = faculties_url

    def get_faculties_url(self):
        return self.faculties_url

    def get_faculties_response(self):
        faculties_req = requests.get(self.faculties_url, verify=False)
        return faculties_req

    def get_faculties_page(self, response):
        try:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "html.parser")
                return page
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        faculties = page.find_all("span", class_="Z3988", limit=13)
        faculties_list = [faculty.string for faculty in faculties]
        return faculties_list


class PucpThesis:
    # https://repositorio.pucp.edu.pe/index/handle/123456789/{value}/browse?type=dateissued
    def __init__(self, thesis_url):
        self.thesis_url = thesis_url
        self.thesis_ids = [9117, 170514, 9118, 129392, 135248, 9119, 9120, 9121, 9122, 9123, 9124, 9125, 129361]

    def get_thesis_url(self):
        return self.thesis_url

    def get_thesis_ids(self):
        return self.thesis_ids

    def get_thesis_response(self):
        thesis_response = deque()
        for thesis in self.thesis_ids:
            thesis_req = requests.get(f"{self.thesis_url}/{thesis}/browse?type=dateissued", verify=False)
            thesis_response.append(thesis_req)
        return thesis_response

    def get_thesis_page(self, responses):
        thesis_pages = deque()

        for response in responses:
            try:
                if response.status_code == 200:
                    page = BeautifulSoup(response.text, "html.parser")
                    thesis_pages.append(page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")
        return thesis_pages

    def get_thesis_position(self, pages):
        thesis_positions_list = deque()

        for page in pages:
            thesis_p = page.find_all("p", class_="pagination-info")
            thesis_string = [thesis.string for thesis in thesis_p]
            thesis_position = thesis_string[0]
            thesis_positions_list.append(thesis_position)
        return thesis_positions_list

    def get_thesis_count(self, positions):
        thesis_count_list = deque()

        for position in positions:
            options = ["Now showing items 1-20 of ", "Now showing items 1-6 of ", "Now showing items 1-15 of "]

            for option in options:
                if option in position:
                    thesis_count = position.replace(option, "")
                    thesis_count_list.append(thesis_count)
        return thesis_count_list


def get_pucp():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from PUCP...")
    faculties_url = PucpFaculties("https://repositorio.pucp.edu.pe/index/handle/123456789/7312")
    faculties_pages = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(faculties_pages)

    thesis_url = PucpThesis("https://repositorio.pucp.edu.pe/index/handle/123456789/")
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_positions = thesis_url.get_thesis_position(thesis_pages)
    thesis_count = thesis_url.get_thesis_count(thesis_positions)

    module.write_csv(faculties_list, thesis_count, "PUCP_BACHELOR.csv")
