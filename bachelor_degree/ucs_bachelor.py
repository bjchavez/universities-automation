from importlib import import_module
from bs4 import BeautifulSoup
import requests


def get_page():
    req = requests.get("https://repositorio.cientifica.edu.pe/handle/20.500.12805/5", verify=False)
    try:
        if req.status_code == 200:
            page = BeautifulSoup(req.text, "html.parser")
            return page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred erorr: {error}")


def get_faculties(page):
    faculties = page.find_all("span", class_="Z3988")
    faculties_string = [faculty.string for faculty in faculties]
    faculties_list = faculties_string[0:5]
    return faculties_list


def get_thesis_count(page):
    thesis = page.find_all("h4", class_="artifact-title")
    thesis_content = [t.contents[2].string for t in thesis]
    thesis_list = []

    for th in thesis_content[0:5]:
        clean_spaces = th.strip()
        remove_brackets = clean_spaces.translate({ord("["): None, ord("]"): None})
        convert_to_int = int(remove_brackets)
        thesis_list.append(convert_to_int)

    return thesis_list


def get_ucs():
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UCS...")
    faculties = get_faculties(get_page())
    thesis = get_thesis_count(get_page())

    module.write_csv(faculties, thesis, "UCS_BACHELOR.csv")
