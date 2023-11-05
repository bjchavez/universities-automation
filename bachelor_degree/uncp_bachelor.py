from bs4 import BeautifulSoup
from importlib import import_module
from collections import deque
import requests
import urllib3


def get_faculties_page():
    req = requests.get("https://repositorio.uncp.edu.pe/", verify=False)
    try:
        if req.status_code == 200:
            faculties_page = BeautifulSoup(req.text, "html.parser")
            return faculties_page
    except requests.exceptions.HTTPError as error:
        print(f"An ocurred error: {error}")


def get_faculties(page):
    faculties = page.find_all("span", class_="Z3988", limit=5)
    faculties_string = [faculty.string for faculty in faculties]
    faculties_list = [faculty.replace(faculty[0:3], "") for faculty in faculties_string]
    faculties_list_clean = [faculty.replace(",", "") for faculty in faculties_list]
    return faculties_list_clean


def get_thesis_count_page():
    thesis_count_page = deque()
    thesis_ids = [[968, 969, 970, 971, 1014, 1016, 1017, 961, 1019, 1018, 1020],
                  [1030, 1027, 1028, 1029, 1031],
                  [4637, 4657, 4671, 4676, 4669, 4647, 4678, 4680, 4673, 4642],
                  [41, 40],
                  [989, 1289, 991, 1710, 1036, 1035, 1037, 1034, 1032, 1033, 2657, 1254, 990, 992]]
    thesis_limits = [[3, 2, 3, 3, 2, 4, 2, 3, 1, 1, 1],
                     [3, 3, 3, 3, 1],
                     [3, 1, 1, 1, 1, 3, 1, 1, 2, 3],
                     [3, 1],
                     [4, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3]]

    for i in range(len(thesis_ids)):
        thesis_to_add = deque()

        for value in zip(thesis_ids[i], thesis_limits[i]):
            req = requests.get(f"https://repositorio.uncp.edu.pe/handle/20.500.12894/{value[0]}", verify=False)
            try:
                if req.status_code == 200:
                    page = BeautifulSoup(req.text, "html.parser")
                    thesis_page = page.find_all("div", class_="artifact-title", limit=value[1])
                    thesis_to_add.append(thesis_page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")

        thesis_count_page.append(thesis_to_add)

    return thesis_count_page
    # print(thesis_count_page)

# def get_thesis_count():
#     thesis_list = deque()
#     thesis_ids = [[968, 969, 970, 971, 1014, 1016, 1017, 961, 1019, 1018, 1020],
#                   [1030, 1027, 1028, 1029, 1031],
#                   [4637, 4657, 4671, 4676, 4669, 4647, 4678, 4680, 4673, 4642],
#                   [41, 40],
#                   [989, 1289, 991, 1710, 1036, 1035, 1037, 1034, 1032, 1033, 2657, 1254, 990, 992]]
#     thesis_limits = [[3, 2, 3, 3, 2, 4, 2, 3, 1, 1, 1],
#                      [3, 3, 3, 3, 1],
#                      [3, 1, 1, 1, 1, 3, 1, 1, 2, 3],
#                      [3, 1],
#                      [4, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3]]
#
#     for i in range(len(thesis_ids)):
#         thesis_to_sum = deque()
#
#         for value in zip(thesis_ids[i], thesis_limits[i]):
#             req = requests.get(f"https://repositorio.uncp.edu.pe/handle/20.500.12894/{value[0]}", verify=False)
#             try:
#                 if req.status_code == 200:
#                     page = BeautifulSoup(req.text, "html.parser")
#                     thesis_page = page.find_all("div", class_="artifact-title", limit=value[1])
#                     thesis_string_list = [thesis_str.contents[2] for thesis_str in thesis_page]
#
#                     if value[0] == 989:
#                         thesis_value = thesis_string_list[1]
#                     elif value[0] == 1014:
#                         thesis_value = thesis_string_list[0]
#                     else:
#                         thesis_value = thesis_string_list[-1]
#
#                     remove_spaces = thesis_value.strip()
#                     remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
#                     convert_to_int = int(remove_brackets)
#                     thesis_to_sum.append(convert_to_int)
#
#             except requests.exceptions.HTTPError as error:
#                 print(f"An error ocurred: {error}")
#
#         thesis_add = sum(thesis_to_sum)
#         thesis_list.append(thesis_add)
#
#     return thesis_list


# def get_uncp():
#     module = import_module("pregrado.utils.thesis")
#
#     print("Getting data from UNCP...")
#     uncp_faculties = get_faculties()
#     uncp_thesis = get_thesis_count()
#
#     module.write_csv(uncp_faculties, uncp_thesis, "UNCP_PREGRADO.csv")


if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    get_thesis_count_page()
