from importlib import import_module
from bs4 import BeautifulSoup
import requests
import re


class Unsch:
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
                page_find = page.find_all(class_=re.compile("heading"))
                return page_find
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        faculties_content = [faculty.contents[0].string for faculty in page]
        faculties_list = faculties_content[1:10]
        return faculties_list

    def get_thesis_count(self, page):
        thesis_content = [thesis.contents[2].string for thesis in page]
        thesis_list = thesis_content[1:10]
        return thesis_list


def get_unsch():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNSCH...")
    unsch = Unsch("http://repositorio.unsch.edu.pe/")
    page = unsch.get_page(unsch.get_response())
    faculties_list = unsch.get_faculties(page)

    thesis_count = unsch.get_thesis_count(page)

    module.write_csv(faculties_list, thesis_count, "UNSCH_BACHELOR.csv")
