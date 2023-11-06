from importlib import import_module
from bs4 import BeautifulSoup
import requests


class Ucs:
    def __init__(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_response(self):
        req = requests.get(self.url, verify=False)
        return req

    def get_page(self, response):
        try:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "html.parser")
                return page
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        faculties = page.find_all("span", class_="Z3988")
        faculties_string = [faculty.string for faculty in faculties]
        faculties_list = faculties_string[0:5]
        return faculties_list

    def get_thesis_positions(self, page):
        thesis = page.find_all("h4", class_="artifact-title")
        thesis_content = [t.contents[2].string for t in thesis]
        return thesis_content

    def get_thesis_count(self, positions):
        thesis_count_list = []

        for position in positions[0:5]:
            clean_spaces = position.strip()
            remove_brackets = clean_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_ucs():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UCS...")
    ucs = Ucs("https://repositorio.cientifica.edu.pe/handle/20.500.12805/5")
    page = ucs.get_page(ucs.get_response())
    faculties_list = ucs.get_faculties(page)

    thesis_position = ucs.get_thesis_positions(page)
    thesis_count = ucs.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UCS_BACHELOR.csv")
