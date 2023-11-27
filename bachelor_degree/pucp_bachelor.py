from importlib import import_module
from bs4 import BeautifulSoup
from collections import deque
import requests


class PucpFaculties:
    """
    This class provides only the methods to get faculties data from PUCP.
    """
    def __init__(self, faculties_url) -> None:
        """
        Args:
            faculties_url[string]: Faculties page URL.
        """
        self.faculties_url = faculties_url

    def get_faculties_url(self) -> str:
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

    def get_faculties_page(self, response) -> BeautifulSoup:
        """
        This method verify if the status code at response is 200.

        Args:
            response[http]: Http response code of the faculties page.

        Returns:
            Beautifulsoup parsed object.

        Raises:
            HTTPErrors: If the status code is not 200, the method returns an HTTP error and halts the program.
        """
        if response.status_code == 200:
            page = BeautifulSoup(response.text, "html.parser")
            return page
        else:
            raise requests.exceptions.HTTPError

    def get_faculties(self, page) -> list[str]:
        """
        This method find all 'span' HTML elements and convert them to strings.

        Args:
            page[beautifulsoup]: Beautifulsoup parsed object.

        Returns:
            A list of strings with the faculties names.
        """
        faculties = page.find_all("span", class_="Z3988", limit=13)
        faculties_list = [faculty.string for faculty in faculties]
        return faculties_list


class PucpThesis:
    """
    This class provides only the methods to get theses data from PUCP.
    """
    def __init__(self, thesis_url) -> None:
        """
        This method initialize a identifiers list for each theses page.

        Args:
            thesis_url[string]: Theses page URL.
        """
        self.thesis_url = thesis_url
        self.thesis_ids = [9117, 170514, 9118, 129392, 135248, 9119, 9120, 9121, 9122, 9123, 9124, 9125, 129361]

    def get_thesis_url(self) -> str:
        """
        Returns:
            The URL of the theses.
        """
        return self.thesis_url

    def get_thesis_ids(self) -> list[int]:
        """
        Returns:
            The list of IDs for the theses.
        """
        return self.thesis_ids

    def get_thesis_response(self) -> list:
        """
        This method make http requests at thesis URL.

        Returns:
            A list of http response codes.
        """
        thesis_response = []
        for thesis in self.thesis_ids:
            thesis_req = requests.get(f"{self.thesis_url}/{thesis}/browse?type=dateissued", verify=False)
            thesis_response.append(thesis_req)
        return thesis_response

    def get_thesis_page(self, responses):
        """
        This method loops through the deque of HTTP responses and verifies if their status code is 200.

        Args:
            responses[deque]: Http response codes of each thesis page.

        Returns:
            A deque of BeautifulSoup parsed objects.

        Raises:
            HTTPErrors: If the status code is not 200, the method returns an HTTP error and halts the program.
        """
        thesis_pages = deque()

        for response in responses:
            if response.status_code == 200:
                page = BeautifulSoup(response.text, "html.parser")
                thesis_pages.append(page)
                return thesis_pages
            else:
                raise requests.exceptions.HTTPError

    def get_thesis_position(self, pages) -> deque[str]:
        """
        This method find all paragraph HTML elements, convert them to strings and select the zero position.

        Args:
            pages[deque]: BeautifulSoup parsed pages.

        Returns:
            A deque of paragraph HTML elements.
        """
        thesis_positions_list = deque()

        for page in pages:
            thesis_p = page.find_all("p", class_="pagination-info")
            thesis_string = [thesis.string for thesis in thesis_p]
            thesis_position = thesis_string[0]
            thesis_positions_list.append(thesis_position)
        return thesis_positions_list

    def get_thesis_count(self, positions) -> deque[int]:
        """
        This method loops through the positions parameter and verifies if there is a match with a list of strings.
        If it is true, it removes the item; otherwise, it breaks.

        Args:
            positions[deque]: Paragraph HTML elements.

        Returns:
            A deque with the numbers of the theses.
        """
        thesis_count_list = deque()

        for position in positions:
            options = ["Now showing items 1-20 of ", "Now showing items 1-6 of ", "Now showing items 1-15 of "]

            for option in options:
                if option in position:
                    thesis_count = position.replace(option, "")
                    thesis_count_list.append(int(thesis_count))
        return thesis_count_list


def get_pucp():
    """
    This method is used to initialize the PUCP class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")

    print("Getting data from PUCP...")
    faculties_url = PucpFaculties("https://repositorio.pucp.edu.pe/index/handle/123456789/7312")
    faculties_pages = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(faculties_pages)

    thesis_url = PucpThesis("https://repositorio.pucp.edu.pe/index/handle/123456789")
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_positions = thesis_url.get_thesis_position(thesis_pages)
    thesis_count = thesis_url.get_thesis_count(thesis_positions)

    module.write_csv(faculties_list, thesis_count, "PUCP_BACHELOR.csv")


faculties_pucp = PucpFaculties("https://repositorio.pucp.edu.pe/index/handle/123456789/7312")
thesis_pucp = PucpThesis("https://repositorio.pucp.edu.pe/index/handle/123456789")
