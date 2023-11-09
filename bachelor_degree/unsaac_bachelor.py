from bs4 import BeautifulSoup
from collections import deque
from importlib import import_module
import requests
import re


class Unsaac:
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
        return faculties_string[3:13]

    def get_thesis_position(self, page):
        thesis = page.find_all(class_=re.compile("mode"))
        thesis_content = [t.contents[2].string for t in thesis]
        return thesis_content[3:13]

    def get_thesis_count(self, positions):
        thesis_count_list = []

        for position in positions:
            remove_spaces = position.strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_unsaac():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNSAAC...")
    unsaac = Unsaac("https://repositorio.unsaac.edu.pe/")
    page = unsaac.get_page(unsaac.get_response())
    faculties_list = unsaac.get_faculties(page)

    thesis_position = unsaac.get_thesis_position(page)
    thesis_count = unsaac.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UNSAAC_BACHELOR.csv")


# def get_page():
#     req = requests.get("https://repositorio.unsaac.edu.pe/", verify=False)
#     try:
#         if req.status_code == 200:
#             page = BeautifulSoup(req.text, "html.parser")
#             return page
#     except requests.exceptions.HTTPError as error:
#         print(f"An ocurred error: {error}")
#
# def get_thesis_count(page):
#     thesis = page.find_all(class_=re.compile("mode"))
#     thesis_content = [t.contents[2].string for t in thesis]
#
#     thesis_list = deque()
#     for t in thesis_content[3:13]:
#         remove_spaces = t.strip()
#         remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
#         convert_to_int = int(remove_brackets)
#         thesis_list.append(convert_to_int)
#
#     return thesis_list
#
#
# def get_unsaac():
#     module = import_module("bachelor_degree.utils.thesis")
#
#     print("Getting data from UNSAAC...")
#     faculties = get_faculties(get_page())
#     thesis = get_thesis_count(get_page())
#
#     module.write_csv(faculties, thesis, "UNSAAC_BACHELOR.csv")
