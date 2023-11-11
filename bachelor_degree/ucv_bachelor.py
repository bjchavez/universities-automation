from importlib import import_module
from bs4 import BeautifulSoup
import requests


class Ucv:
    """
    This class provides the methods to get faculties and theses data from UCV.
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
        This method find all 'span' HTML elements and convert them to strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list of strings.
        """
        faculties = page.find_all("span", class_="Z3988", limit=4)
        faculties_list = [faculty.string for faculty in faculties]
        return faculties_list

    def get_thesis_positions(self, page):
        """
        This method find all 'h4' HTML elements, locate the lasts and convert them to strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list with the positions of the theses.
        """
        thesis = page.find_all("h4", class_="artifact-title", limit=4)
        thesis_string = [t.contents[2].string for t in thesis]
        return thesis_string

    def get_thesis_count(self, positions):
        """
        This method loops over the positions, removes all blank spaces and brackets, and converts them to integers.

        Args:
            positions[list]: List of strings with the positions of the theses.

        Returns:
            A list of integers with the numbers of each thesis.
        """
        thesis_count_list = []

        for position in positions:
            remove_spaces = position.lstrip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_ucv():
    """
    This method is used to initialize the UCV class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UCV...")
    ucv = Ucv("https://repositorio.ucv.edu.pe/handle/20.500.12692/4")
    page = ucv.get_page(ucv.get_response())
    faculties_list = ucv.get_faculties(page)

    thesis_position = ucv.get_thesis_positions(page)
    thesis_count = ucv.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UCV_BACHELOR.csv")
