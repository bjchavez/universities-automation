from bs4 import BeautifulSoup
from collections import deque
from importlib import import_module
import requests
import re


def get_page():
    req = requests.get("https://repositorio.unsaac.edu.pe/", verify=False)
    try:
        if req.status_code == 200:
            page = BeautifulSoup(req.text, "html.parser")
            return page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("a", attrs={"name": "community-browser-link"})
    faculties_string = [faculty.string for faculty in faculties]
    faculties_list = faculties_string[3:13]
    return faculties_list


def get_thesis_count(page):
    thesis = page.find_all(class_=re.compile("mode"))
    thesis_content = [t.contents[2].string for t in thesis]

    thesis_list = deque()
    for t in thesis_content[3:13]:
        remove_spaces = t.strip()
        remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
        convert_to_int = int(remove_brackets)
        thesis_list.append(convert_to_int)

    return thesis_list


def get_unsaac():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNSAAC...")
    faculties = get_faculties(get_page())
    thesis = get_thesis_count(get_page())

    module.write_csv(faculties, thesis, "UNSAAC_BACHELOR.csv")
