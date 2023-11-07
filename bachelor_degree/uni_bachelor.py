from bs4 import BeautifulSoup
from importlib import import_module
import requests


class UniFaculties:
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
                page = BeautifulSoup(response.text, "xml")
                return page
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        faculties = page.find_all("h4", class_="list-group-item-heading", limit=11)
        faculties_content = [f.contents[0].string for f in faculties]
        faculties_list = [f.strip() for f in faculties_content]
        return faculties_list


class UniThesis:
    def __init__(self, thesis_url):
        self.thesis_url = thesis_url
        self.thesis_ids = [2, 56, 17, 12, 36, 23, 29, 49, 43, 79, 87]

    def get_thesis_url(self):
        return self.thesis_url

    def get_thesis_ids(self):
        return self.thesis_ids

    def get_thesis_response(self):
        thesis_response = []

        for thesis in self.thesis_ids:
            thesis_req = requests.get(f"{self.thesis_url}/{thesis}", verify=False)
            thesis_response.append(thesis_req)
        return thesis_response

    def get_thesis_page(self, responses):
        thesis_pages = []

        for response in responses:
            try:
                if response.status_code == 200:
                    page = BeautifulSoup(response.text, "xml")
                    thesis_pages.append(page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")
        return thesis_pages

    def get_thesis_position(self, pages):
        thesis_positions = []

        for page in pages:
            thesis_find = page.find_all("h4", class_="list-group-item-heading")
            thesis_content = [thesis.contents[1] for thesis in thesis_find]
            thesis_positions.append(thesis_content[1:])
        return thesis_positions

    def get_thesis_count(self, positions):
        thesis_count_list = []

        for position_list in positions:
            recovered_count = []

            for position in position_list:
                remove_spaces = position.strip()
                remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
                convert_to_int = int(remove_brackets)
                recovered_count.append(convert_to_int)
            thesis_count_list.append(sum(recovered_count))
        return thesis_count_list


def get_uni():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNI...")
    faculties_url = UniFaculties("https://cybertesis.uni.edu.pe/handle/20.500.14076/1")
    faculties_page = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(faculties_page)

    thesis_url = UniThesis("https://cybertesis.uni.edu.pe/handle/20.500.14076")
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_positions = thesis_url.get_thesis_position(thesis_pages)
    thesis_count = thesis_url.get_thesis_count(thesis_positions)

    module.write_csv(faculties_list, thesis_count, "UNI_BACHELOR.csv")
