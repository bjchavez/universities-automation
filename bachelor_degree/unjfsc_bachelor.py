from bs4 import BeautifulSoup
from importlib import import_module
import requests
import re


class Unjfsc:
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
        faculties = page.find_all("a", attrs={"name": "community-browser-link"})
        faculties_string = [faculty.string for faculty in faculties]
        faculties_comma = [f.translate({ord(","): None}) for f in faculties_string]
        return faculties_comma[2:15]

    def get_thesis_position(self, page):
        thesis = page.find_all(class_=re.compile("mode"))
        thesis_content = [t.contents[2].string for t in thesis]
        return thesis_content[2:15]

    def get_thesis_count(self, positions):
        thesis_count_list = []

        for position in positions:
            remove_spaces = position.strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_unjfsc():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNJFSC...")
    unjfsc = Unjfsc("http://repositorio.unjfsc.edu.pe/")
    page = unjfsc.get_page(unjfsc.get_response())
    faculties_list = unjfsc.get_faculties(page)

    thesis_position = unjfsc.get_thesis_position(page)
    thesis_count = unjfsc.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UNJFSC_BACHELOR.csv")
