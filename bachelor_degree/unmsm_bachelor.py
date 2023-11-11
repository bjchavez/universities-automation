from bs4 import BeautifulSoup
from importlib import import_module
import requests


class UnmsmFaculties:
    """
    This class provides only the methods to get faculties data from UNMSM.
    """
    def __init__(self, faculties_url):
        """
        This method initializes two lists, one for identifiers and another for limits; each index references
        one page of the faculties.

        Args:
            faculties_url[string]: Faculties page URL.
        """
        self.faculties_url = faculties_url
        self.faculties_ids = [1, 2, 3, 4, 5]
        self.faculties_limits = [4, 5, 3, 4, 4]

    def get_faculties_url(self):
        """
        Returns:
            The URL of the faculties.
        """
        return self.faculties_url

    def get_faculties_ids(self):
        """
        Returns:
            The list of faculties IDs.
        """
        return self.faculties_ids

    def get_faculties_limits(self):
        """
        Returns:
            The list of faculties limits.
        """
        return self.get_faculties_limits

    def get_faculties_response(self):
        """
        This method compresses two lists, loops through them, and makes https requests at faculties URL's.

        Returns:
            A list of http response codes.
        """
        faculties_responses = []

        for value in zip(self.faculties_ids, self.faculties_limits):
            faculties_req = requests.get(f"{self.faculties_url}/{value[0]}", verify=False)
            faculties_responses.append(faculties_req)
        return faculties_responses

    def get_faculties_page(self, responses):
        """
        This method loops through the responses and verifies if their status code is 200.

        Args:
            responses[list]: Http response codes of the faculties pages.

        Returns:
            A list of BeatifulSoup parsed pages.
        """
        faculties_pages = []

        for response in responses:
            try:
                if response.status_code == 200:
                    faculties_page = BeautifulSoup(response.text, "html.parser")
                    faculties_pages.append(faculties_page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")
        return faculties_pages

    def get_faculties(self, pages):
        """
        This method compresses two lists, the pages and limits; finds all 'h4' HTML elements, locates and removes all commas.
        Then, it appends them to a list and returns it.

        Args:
            pages[list]: BeatifulSoup parsed pages.

        Returns:
            A list of strings with all names of the faculties.
        """
        faculties_list = []

        for value in zip(pages, self.faculties_limits):
            faculties_find = value[0].find_all("h4", class_="artifact-title", limit=value[1])
            faculties_content = [content.contents[1].string for content in faculties_find]
            faculties_comma = [f.translate({ord(","): None}) for f in faculties_content]

            for faculty in faculties_comma:
                faculties_list.append(faculty)
        return faculties_list


class UnmsmThesis:
    """
    This class provides only the methods to get theses data from UNMSM.
    """
    def __init__(self, thesis_url):
        """
        This method initialize two lists, one for identifiers and another for limits; each index references
        one page of the theses.

        Args:
            thesis_url[string]: Theses page URL.
        """
        self.thesis_url = thesis_url
        self.thesis_ids = [6, 8, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        self.thesis_limits = [3, 2, 4, 3, 3, 5, 1, 1, 1, 3, 3, 3, 6, 2, 2, 8, 2, 3, 5, 3]

    def get_thesis_url(self):
        """
        Returns:
            The URL of the theses.
        """
        return self.thesis_url

    def get_thesis_ids(self):
        """
        Returns:
            The list of thesis identifiers.
        """
        return self.thesis_ids

    def get_thesis_limits(self):
        """
        Returns:
            The list of thesis limits.
        """
        return self.thesis_limits

    def get_thesis_response(self):
        """
        This method make http requests at thesis URL.

        Returns:
            A list of http response codes.
        """
        thesis_responses = []

        for value in zip(self.thesis_ids, self.thesis_limits):
            thesis_req = requests.get(f"{self.thesis_url}/{value[0]}", verify=False)
            thesis_responses.append(thesis_req)
        return thesis_responses

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
                    thesis_page = BeautifulSoup(response.text, "html.parser")
                    thesis_pages.append(thesis_page)
            except requests.exceptions.HTTPError as error:
                print(f"An ocurred error: {error}")
        return thesis_pages

    def get_thesis_count(self, pages):
        """
        This method compresses two lists, the pages and limits; finds all 'h4' HTML elements and locate the last element.
        We convert it to string, then loop over the list, removing spaces and brackets. Finally, we convert to integer
        and add it to a new list that will be returned.

        Args:
            pages[list]: BeautifulSoup parsed objects.

        Returns:
            A list of integers with all numbers of the theses.
        """
        thesis_count_list = []

        for value in zip(pages, self.thesis_limits):
            thesis_find = value[0].find_all("h4", class_="artifact-title", limit=value[1])
            thesis_content = [content.contents[2].string for content in thesis_find]
            thesis_to_sum = []

            for thesis in thesis_content:
                remove_spaces = thesis.strip()
                remove_brackets = remove_spaces.translate({ord("["): None, ord("]"): None})
                convert_to_int = int(remove_brackets)
                thesis_to_sum.append(convert_to_int)

            thesis_count_list.append(sum(thesis_to_sum))
        return thesis_count_list


def get_unmsm():
    """
    This method is used to initialize the UNMSM class objects and write the CSV file.
    """
    module = import_module("bachelor_degree.utils.thesis")
    url = "https://cybertesis.unmsm.edu.pe/handle/20.500.12672"

    print("Getting data from UNMSM...")
    faculties_url = UnmsmFaculties(url)
    faculties_pages = faculties_url.get_faculties_page(faculties_url.get_faculties_response())
    faculties_list = faculties_url.get_faculties(faculties_pages)

    thesis_url = UnmsmThesis(url)
    thesis_pages = thesis_url.get_thesis_page(thesis_url.get_thesis_response())
    thesis_count = thesis_url.get_thesis_count(thesis_pages)

    module.write_csv(faculties_list, thesis_count, "UNMSM_BACHELOR.csv")
