from bs4 import BeautifulSoup
from collections import deque
from importlib import import_module
import requests
import itertools


def get_faculties_page():
    req = requests.get("https://cybertesis.uni.edu.pe/handle/20.500.14076/1", verify=False)
    try:
        if req.status_code == 200:
            page = BeautifulSoup(req.text, "xml")
            return page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("h4", class_="list-group-item-heading", limit=11)
    faculties_content = [f.contents[0].string for f in faculties]
    faculties_list = [f.strip() for f in faculties_content]
    return faculties_list


def get_thesis_count_pages():
    thesis_ids = [2, 56, 17, 12, 36, 23, 29, 49, 43, 79, 87]
    thesis_count_pages = []

    for id in thesis_ids:
        req = requests.get(f"https://cybertesis.uni.edu.pe/handle/20.500.14076/{id}", verify=False)
        try:
            if req.status_code == 200:
                thesis_page = BeautifulSoup(req.text, "xml")
                thesis_count_pages.append(thesis_page)
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    return thesis_count_pages


def get_thesis_count(pages):
    thesis_count_list = []

    for page in pages:
        thesis_find = page.find_all("h4", class_="list-group-item-heading")
        thesis_content = [thesis.contents[1] for thesis in thesis_find]
        thesis_recovered = []

        for thesis in thesis_content:
            remove_spaces = thesis.strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_recovered.append(convert_to_int)

        thesis_sum = deque(itertools.islice(thesis_recovered, 1, 10))
        thesis_count_list.append(sum(thesis_sum))

    return thesis_count_list


def get_uni():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNI...")
    faculties = get_faculties(get_faculties_page())
    thesis = get_thesis_count(get_thesis_count_pages())

    module.write_csv(faculties, thesis, "UNI_BACHELOR.csv")
