from collections import deque
import csv


def write_csv(faculties: list | deque, thesis: list | deque, csv_name: str):
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
