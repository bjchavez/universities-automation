from importlib import import_module
from bs4 import BeautifulSoup
from collections import deque
import requests


class UnalmFaculties:
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
        faculties = page.find_all("a", attrs={"name": "community-browser-link"}, limit=8)
        faculties_list = [faculty.string for faculty in faculties]
        return faculties_list


class UnalmThesis:
    def __init__(self, thesis_url):
        self.thesis_url = thesis_url
        self.thesis_ids = [[12, 13, 14, 15, 16],
                           [17, 18, 19, 20],
                           [21, 22],
                           [23, 25, 26, 24],
                           [27, 28],
                           [29, 30, 31],
                           [32, 33],
                           [192, 34]]

    def get_thesis_url(self):
        return self.thesis_url

    def get_thesis_response(self):
        thesis_responses = deque()

        for i in range(len(self.thesis_ids)):
            recovered_responses = deque()

            for thesis_id in self.thesis_ids[i]:
                req = requests.get(f"{self.thesis_url}/{thesis_id}", verify=False)
                recovered_responses.append(req)

            thesis_responses.append(recovered_responses)
        return thesis_responses

    def get_thesis_page(self, responses):
        thesis_pages = deque()

        for i in range(len(responses)):
            recovered_pages = deque()

            for response in responses[i]:
                try:
                    if response.status_code == 200:
                        page = BeautifulSoup(response.text, "html.parser")
                        recovered_pages.append(page)
                except requests.exceptions.HTTPError as error:
                    print(f"An ocurred error: {error}")

            thesis_pages.append(recovered_pages)
        return thesis_pages

    def get_thesis_position(self, pages):
        thesis_positions = deque()

        for i in range(len(pages)):
            recovered_positions = deque()

            for page in pages[i]:
                thesis = page.find_all("h4", class_="artifact-title", limit=5)
                thesis_content = [t.contents[2] for t in thesis]
                recovered_positions.append(thesis_content)

            thesis_positions.append(recovered_positions)
        return thesis_positions

    def get_thesis_count(self, positions):
        thesis_count = deque()

        for i in range(len(positions)):
            recovered_count = deque()

            for position in positions[i]:
                remove_spaces = position[-1].strip()
                remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
                convert_to_int = int(remove_brackets)
                recovered_count.append(convert_to_int)

            count_added = sum(recovered_count)
            thesis_count.append(count_added)

        return thesis_count


def get_unalm():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNALM...")
    faculties_url = UnalmFaculties("https://repositorio.lamolina.edu.pe/")
    falcuties_page = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(falcuties_page)

    thesis_url = UnalmThesis("https://repositorio.lamolina.edu.pe/handle/20.500.12996")
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_positions = thesis_url.get_thesis_position(thesis_pages)
    thesis_count = thesis_url.get_thesis_count(thesis_positions)

    module.write_csv(faculties_list, thesis_count, "UNALM_BACHELOR.csv")
