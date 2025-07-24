import csv
import sys
from itertools import islice


def read_cars_data(filename):
    def convert_row_to_tuple(row):
        return (row[0], float(row[1]))

    def is_valid_row(row):
        return len(row) == 2 and row[1].isdigit()

    with open(filename, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        rows = list(islice(csv_reader, 1, None))

        return list(map(convert_row_to_tuple, filter(is_valid_row, rows)))


def filter_cars(max_emission, cars):
    return list(filter(lambda car: car[1] < max_emission, cars))


def sort_cars(cars):
    return sorted(cars, key=lambda x: x[1])


cars_data = read_cars_data("cars_data.csv")
sorted_cars = sort_cars(cars_data)

print("All cars (sorted by emission): ")
print(sorted_cars)

max_permitted_value = float('inf')

try:
    max_permitted_value = float(
        input("Please enter a max permitted emission g/km. Example: 20: "))
except ValueError:
    print('Value must be a number, idiot!')
    sys.exit()

filtered_cars = sort_cars(filter_cars(max_permitted_value, cars_data))

print('Cars that meet your criteria: ')
print(filtered_cars)
