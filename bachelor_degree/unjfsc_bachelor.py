from bs4 import BeautifulSoup
from importlib import import_module
import requests
import re


class Unjfsc:
    """
    This class provides the methods to get faculties and theses data from UNJFSC.
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
        This method find all 'a' HTML elements, convert them to strings and remove all commas.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list of strings with the faculties names.
        """
        faculties = page.find_all("a", attrs={"name": "community-browser-link"})
        faculties_string = [faculty.string for faculty in faculties]
        faculties_comma = [f.translate({ord(","): None}) for f in faculties_string]
        return faculties_comma[2:15]

    def get_thesis_position(self, page):
        """
        This method find all 'mode' CSS classes, locate the lasts and convert them to strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list with the positions of the theses.
        """
        thesis = page.find_all(class_=re.compile("mode"))
        thesis_content = [t.contents[2].string for t in thesis]
        return thesis_content[2:15]

    def get_thesis_count(self, positions):
        """
        This method loops over the positions, removes all blank spaces and brackets, and converts them to integers.

        Args:
            positions[list]: Positions of the theses.

        Returns:
            A list of integers with the numbers of each thesis.
        """
        thesis_count_list = []

        for position in positions:
            remove_spaces = position.strip()
            remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
            convert_to_int = int(remove_brackets)
            thesis_count_list.append(convert_to_int)
        return thesis_count_list


def get_unjfsc():
    """
    This method is used to initialize the UNJFSC class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNJFSC...")
    unjfsc = Unjfsc("http://repositorio.unjfsc.edu.pe/")
    page = unjfsc.get_page(unjfsc.get_response())
    faculties_list = unjfsc.get_faculties(page)

    thesis_position = unjfsc.get_thesis_position(page)
    thesis_count = unjfsc.get_thesis_count(thesis_position)

    module.write_csv(faculties_list, thesis_count, "UNJFSC_BACHELOR.csv")
