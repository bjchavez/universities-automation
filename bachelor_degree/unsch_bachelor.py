from importlib import import_module
from bs4 import BeautifulSoup
import requests
import re


def get_page():
    req = requests.get("http://repositorio.unsch.edu.pe/", verify=False)
    try:
        if req.status_code == 200:
            page = BeautifulSoup(req.text, "html.parser")
            page_find = page.find_all(class_=re.compile("heading"))
            return page_find
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties_content = [faculty.contents[0].string for faculty in page]
    faculties_list = faculties_content[1:10]
    return faculties_list


def get_thesis_count(page):
    thesis_content = [thesis.contents[2].string for thesis in page]
    thesis_list = thesis_content[1:10]
    return thesis_list


def get_unsch():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNSCH...")
    faculties = get_faculties(get_page())
    thesis = get_thesis_count(get_page())

    module.write_csv(faculties, thesis, "UNSCH_BACHELOR.csv")
