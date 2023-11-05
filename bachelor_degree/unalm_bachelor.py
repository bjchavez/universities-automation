from importlib import import_module
from bs4 import BeautifulSoup
from collections import deque
import requests


def get_faculties_page():
    req = requests.get("https://repositorio.lamolina.edu.pe/", verify=False)
    try:
        if req.status_code == 200:
            faculties_page = BeautifulSoup(req.text, "html.parser")
            return faculties_page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("a", attrs={"name": "community-browser-link"}, limit=8)
    faculties_list = [faculty.string for faculty in faculties]
    return faculties_list


def get_thesis_count_page():
    thesis_count_pages = []
    thesis_ids = [[12, 13, 14, 15, 16],
                  [17, 18, 19, 20],
                  [21, 22],
                  [23, 25, 26, 24],
                  [27, 28],
                  [29, 30, 31],
                  [32, 33],
                  [192, 34]]

    for i in range(len(thesis_ids)):
        thesis_recovered_page = []
        for id in thesis_ids[i]:
            req = requests.get(f"https://repositorio.lamolina.edu.pe/handle/20.500.12996/{id}", verify=False)
            try:
                if req.status_code == 200:
                    thesis_page = BeautifulSoup(req.text, "html.parser")
                    thesis_recovered_page.append(thesis_page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")

        thesis_count_pages.append(thesis_recovered_page)

    return thesis_count_pages


def get_thesis_count(pages):
    thesis_list = deque()

    for i in range(8):
        thesis_recovered = deque()

        for page in pages[i]:
            thesis = page.find_all("h4", class_="artifact-title", limit=5)
            thesis_count = [t.contents[2] for t in thesis]

            remove_spaces = thesis_count[-1].strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_recovered.append(convert_to_int)

        thesis_sum = sum(thesis_recovered)
        thesis_list.append(thesis_sum)

    return thesis_list


def get_unalm():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNALM...")
    faculties = get_faculties(get_faculties_page())
    thesis = get_thesis_count(get_thesis_count_page())

    module.write_csv(faculties, thesis, "UNALM_BACHELOR.csv")
