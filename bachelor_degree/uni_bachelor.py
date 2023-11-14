from bs4 import BeautifulSoup
from importlib import import_module
import requests


class UniFaculties:
    """
    This class provides only the methods to get faculties data from UNI.
    """
    def __init__(self, faculties_url):
        """
        Args:
            faculties_url[string]: Faculties page URL.
        """
        self.faculties_url = faculties_url

    def get_faculties_url(self):
        """
        Returns:
            The URL of the faculties.
        """
        return self.faculties_url

    def get_faculties_response(self):
        """
        This method make a http request at faculties URL.

        Returns:
            A Http response code.
        """
        faculties_req = requests.get(self.faculties_url, verify=False)
        return faculties_req

    def get_faculties_page(self, response):
        """
        This method verify if the status code is 200.

        Args:
            response[http]: Http response code of the faculties page.

        Returns:
            Beautifulsoup parsed object.

        Raises:
            HTTPErrors: If the status code is not 200, the method returns an HTTP error and halts the program.
        """
        try:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "xml")
                return page
        except requests.exceptions.HTTPError as error:
            print(f"An ocurred error: {error}")

    def get_faculties(self, page):
        """
        This method find all 'h4' HTML elements, locates the firsts, convert them to strings and remove blank spaces.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed object.

        Returns:
            A list of strings with the faculties names.
        """
        faculties = page.find_all("h4", class_="list-group-item-heading", limit=11)
        faculties_content = [f.contents[0].string for f in faculties]
        faculties_list = [f.strip() for f in faculties_content]
        return faculties_list


class UniThesis:
    """
    This class provides only the methods to get theses data from UNI.
    """
    def __init__(self, thesis_url):
        """
        This method initialize a identifiers list of each thesis page.

        Args:
            thesis_url[string]: Theses page URL.
        """
        self.thesis_url = thesis_url
        self.thesis_ids = [2, 56, 17, 12, 36, 23, 29, 49, 43, 79, 87]

    def get_thesis_url(self):
        """
        Returns:
            The URL of the theses.
        """
        return self.thesis_url

    def get_thesis_ids(self):
        """
        Returns:
            The list of IDs for the theses.
        """
        return self.thesis_ids

    def get_thesis_response(self):
        """
        This method make http requests at thesis URL.

        Returns:
            A list of http response codes.
        """
        thesis_response = []

        for thesis in self.thesis_ids:
            thesis_req = requests.get(f"{self.thesis_url}/{thesis}", verify=False)
            thesis_response.append(thesis_req)
        return thesis_response

    def get_thesis_page(self, responses):
        """
        This method loops through the list of HTTP responses and verifies if their status code is 200.

        Args:
            responses[list]: Http response codes of each thesis page.

        Returns:
            A list of BeautifulSoup parsed objects.

        Raises:
            HTTPErrors: If the status code is not 200, the method returns an HTTP error and halts the program.
        """
        thesis_pages = []

        for response in responses:
            try:
                if response.status_code == 200:
                    page = BeautifulSoup(response.text, "xml")
                    thesis_pages.append(page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")
        return thesis_pages

    def get_thesis_position(self, pages):
        """
        This method find all 'h4' HTML elements, we to select the first position and it add to a new list.

        Args:
            pages[list]: BeautifulSoup parsed pages.

        Returns:
            A list of string lists with the thesis positions.
        """
        thesis_positions = []

        for page in pages:
            thesis_find = page.find_all("h4", class_="list-group-item-heading")
            thesis_content = [thesis.contents[1] for thesis in thesis_find]
            thesis_positions.append(thesis_content[1:])
        return thesis_positions

    def get_thesis_count(self, positions):
        """
        This method loops through the positions parameter lists.

        Args:
            positions: String lists with the thesis positions.

        Returns:
            A integers list of the thesis numbers.
        """
        thesis_count_list = []

        for position_list in positions:
            recovered_count = []

            for position in position_list:
                remove_spaces = position.strip()
                remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
                convert_to_int = int(remove_brackets)
                recovered_count.append(convert_to_int)
            thesis_count_list.append(sum(recovered_count))
        return thesis_count_list


def get_uni():
    """
    This method is used to initialize the PUCP class objects and write the UNI file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from UNI...")
    faculties_url = UniFaculties("https://cybertesis.uni.edu.pe/handle/20.500.14076/1")
    faculties_page = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(faculties_page)

    thesis_url = UniThesis("https://cybertesis.uni.edu.pe/handle/20.500.14076")
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_positions = thesis_url.get_thesis_position(thesis_pages)
    thesis_count = thesis_url.get_thesis_count(thesis_positions)

    module.write_csv(faculties_list, thesis_count, "UNI_BACHELOR.csv")
