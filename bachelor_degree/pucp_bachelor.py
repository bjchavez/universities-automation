from importlib import import_module
from bs4 import BeautifulSoup
from collections import deque
import requests


def get_faculties_page():
    faculties_req = requests.get("https://repositorio.pucp.edu.pe/index/handle/123456789/7312", verify=False)
    try:
        if faculties_req.status_code == 200:
            faculties_page = BeautifulSoup(faculties_req.text, "html.parser")
            return faculties_page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("span", class_="Z3988", limit=13)
    faculties_list = [faculty.string for faculty in faculties]
    return faculties_list


def get_thesis_count_pages():
    thesis_count_page = deque()
    page_ids = [9117, 170514, 9118, 129392, 135248, 9119, 9120, 9121, 9122,
                9123, 9124, 9125, 129361]

    for value in page_ids:
        thesis_request = requests.get(f"https://repositorio.pucp.edu.pe/index/handle/123456789/{value}/browse?type=dateissued", verify=False)
        try:
            if thesis_request.status_code == 200:
                thesis_page = BeautifulSoup(thesis_request.text, "html.parser")
                thesis_count_page.append(thesis_page)
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    return thesis_count_page


def get_thesis_count(pages):
    thesis_list = deque()

    for page in pages:
        thesis_paragraph_list = page.find_all("p", class_="pagination-info")
        thesis_string_list = [thesis.string for thesis in thesis_paragraph_list]
        thesis_string = thesis_string_list[0]
        options = ["Now showing items 1-20 of ",
                   "Now showing items 1-6 of ",
                   "Now showing items 1-15 of "]
        for option in options:
            if option in thesis_string:
                thesis_count = thesis_string.replace(option, "")
                thesis_list.append(int(thesis_count))

    return thesis_list


def get_pucp():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from PUCP...")
    faculties = get_faculties(get_faculties_page())
    thesis = get_thesis_count(get_thesis_count_pages())

    module.write_csv(faculties, thesis, "PUCP_BACHELOR.csv")
