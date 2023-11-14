from importlib import import_module
from bs4 import BeautifulSoup
import requests
import re


class Unsch:
    """
    This class provides the methods to get faculties and theses data from UNSCH.
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
        This method verfifies if the status code of the parameter response is 200 and finds all classes 'heading' using the
        re-compile library from python core.

        Args:
            response[http]: Http response code.

        Returns:
            A BeautifulSoup parsed page.

        Raises:
            HTTPErrors: If the status code is not 200, the method returns an HTTP error and halts the program.
        """
        try:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "html.parser")
                page_find = page.find_all(class_=re.compile("heading"))
                return page_find
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        """
        This method locates the position zero at 'page' parameter and converts it to a strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list of strings with the faculties names.
        """
        faculties_content = [faculty.contents[0].string for faculty in page]
        faculties_list = faculties_content[1:10]
        return faculties_list

    def get_thesis_count(self, page):
        """
        This method locates the position two at 'page' parameter and converts it to a strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed page.

        Returns:
            A list of integeres or strings with the theses numbers.
        """
        thesis_content = [thesis.contents[2].string for thesis in page]
        thesis_list = thesis_content[1:10]
        return thesis_list


def get_unsch():
    """
    This method is used to initialize the UNSCH class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNSCH...")
    unsch = Unsch("http://repositorio.unsch.edu.pe/")
    page = unsch.get_page(unsch.get_response())
    faculties_list = unsch.get_faculties(page)

    thesis_count = unsch.get_thesis_count(page)

    module.write_csv(faculties_list, thesis_count, "UNSCH_BACHELOR.csv")
