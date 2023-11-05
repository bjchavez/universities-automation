from bs4 import BeautifulSoup
from collections import deque
from importlib import import_module
import requests


def get_faculties_pages():
    faculties_pages_list = []
    faculties_ids_limits = {1: 4, 2: 5, 3: 3, 4: 4, 5: 4}

    for k, v in faculties_ids_limits.items():
        req = requests.get(f"https://cybertesis.unmsm.edu.pe/handle/20.500.12672/{k}", verify=False)
        try:
            if req.status_code == 200:
                faculties_page = BeautifulSoup(req.text, "html.parser")
                faculties_find = faculties_page.find_all("h4", class_="artifact-title", limit=v)
                faculties_pages_list.append(faculties_find)
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    return faculties_pages_list


def get_faculties(pages):
    faculties_list = []

    for page in pages:
        faculties_content = [content.contents[1].string for content in page]
        faculties_comma = [f.translate({ord(","): None}) for f in faculties_content]

        for faculty in faculties_comma:
            faculties_list.append(faculty)

    return faculties_list


def get_thesis_count_pages():
    thesis_count_pages_list = []
    thesis_ids_limits = {6: 3, 8: 2, 7: 4, 9: 3, 10: 3, 11: 5, 12: 1,
                         13: 1, 14: 1, 15: 3, 16: 3, 17: 3, 18: 6, 19: 2,
                         20: 2, 21: 8, 22: 2, 23: 3, 24: 5, 25: 3}

    for k, v in thesis_ids_limits.items():
        req = requests.get(f"https://cybertesis.unmsm.edu.pe/handle/20.500.12672/{k}", verify=False)
        try:
            if req.status_code == 200:
                thesis_page = BeautifulSoup(req.text, "html.parser")
                thesis_find = thesis_page.find_all("h4", class_="artifact-title", limit=v)
                thesis_count_pages_list.append(thesis_find)
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    return thesis_count_pages_list


def get_thesis_count(pages):
    thesis_list = deque()

    for page in pages:
        thesis_content = [content.contents[2].string for content in page]
        thesis_to_sum = deque()

        for t in thesis_content:
            remove_spaces = t.strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_to_sum.append(convert_to_int)

        thesis_sum = sum(thesis_to_sum)
        thesis_list.append(thesis_sum)

    return thesis_list


def get_unmsm():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNMSM...")
    faculties = get_faculties(get_faculties_pages())
    thesis = get_thesis_count(get_thesis_count_pages())

    module.write_csv(faculties, thesis, "UNMSM_BACHELOR.csv")
