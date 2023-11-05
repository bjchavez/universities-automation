from importlib import import_module
from bs4 import BeautifulSoup
import requests


def get_page():
    req = requests.get("https://repositorio.ucv.edu.pe/handle/20.500.12692/4", verify=False)
    try:
        if req.status_code == 200:
            page = BeautifulSoup(req.text, "html.parser")
            return page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("span", class_="Z3988", limit=4)
    faculties_list = [faculty.string for faculty in faculties]
    return faculties_list


def get_thesis_count(page):
    thesis = page.find_all("h4", class_="artifact-title", limit=4)
    thesis_string = [t.contents[2].string for t in thesis]

    thesis_list = []

    for thesis in thesis_string:
        remove_spaces = thesis.lstrip()
        remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
        convert_to_int = int(remove_brackets)
        thesis_list.append(convert_to_int)

    return thesis_list


def get_ucv():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UCV...")
    faculties = get_faculties(get_page())
    thesis = get_thesis_count(get_page())

    module.write_csv(faculties, thesis, "UCV_BACHELOR.csv")
