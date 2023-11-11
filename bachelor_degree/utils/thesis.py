from collections import deque
import csv


def write_csv(faculties: list | deque, thesis: list | deque, csv_name: str):
    """
    This method will be imported. It works to write to a csv file with the data from universities
    (numbers of faculties and theses).

    Args:
        faculties[list | deque]: A list unknown of faculties.
        thesis[list | deque]: A list unnknown of theses.
        csv_name[string]: It will be the name of csv file.

    Return:
        A csv file writed with the data from universities.
    """
    print("Writing csv file...")
    faculties_thesis_list = list(zip(faculties, thesis))
    try:
        with open(f"bachelor_degree/datasets/{csv_name}", mode="w") as f:
            writer = csv.writer(f)
            writer.writerow(["facultad", "total_tesis"])
            writer.writerows(faculties_thesis_list)
            print("Successfully generated csv file")

    except FileNotFoundError as error:
        print(f"An error ocurred: {error}")
