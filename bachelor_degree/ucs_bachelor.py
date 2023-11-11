from importlib import import_module
from bs4 import BeautifulSoup
import requests


class Ucs:
    """
    This class provides the methods to get faculties and theses data from UCS.
    """
    def __init__(self, url):
        """
        Args:
            url[string]: University URL.
        """
        self.url = url

    def get_url(self):
        """
        Returns:
            The URL of the university.
        """
        return self.url

    def get_response(self):
        """
        This method make http request at university URL.

        Returns:
            One http response code
        """
        req = requests.get(self.url, verify=False)
        return req

    def get_page(self, response):
        """
        This method verfify if the status code of the parameter response is 200.

        Args:
            response[http]: Http response code.

        Returns:
            A BeautifulSoup parsed page.
        """
        try:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "html.parser")
                return page
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        """
        This method find all 'span' HTML elements, convert them to strings and locate the last.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list of strings.
        """
        faculties = page.find_all("span", class_="Z3988")
        faculties_string = [faculty.string for faculty in faculties]
        faculties_list = faculties_string[0:5]
        return faculties_list

    def get_thesis_positions(self, page):
        """
        This method find all 'h4' HTML elements, locate the lasts and convert them to strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list with the positions of the theses.
        """
        thesis = page.find_all("h4", class_="artifact-title")
        thesis_content = [t.contents[2].string for t in thesis]
        return thesis_content

    def get_thesis_count(self, positions):
        """
        This method loops over the positions, removes all blank spaces and brackets, and converts them to integers.

        Args:
            positions[list]: List of strings.

        Returns:
            A list of integers with the numbers of each thesis.
        """
        thesis_count_list = []

        for position in positions[0:5]:
            clean_spaces = position.strip()
            remove_brackets = clean_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_ucs():
    """
    This method is used to initialize the UCS class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UCS...")
    ucs = Ucs("https://repositorio.cientifica.edu.pe/handle/20.500.12805/5")
    page = ucs.get_page(ucs.get_response())
    faculties_list = ucs.get_faculties(page)

    thesis_position = ucs.get_thesis_positions(page)
    thesis_count = ucs.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UCS_BACHELOR.csv")
