import csv
import statistics

# todo: simplify calculations inside this function


def liter_per_kilometer_to_mpg(l_per_k_consumption):
    MILE = 1.609  # kilometers
    GALLON = 3.785  # liters
    consumption_per_one_km = l_per_k_consumption / 100
    consumption_per_one_mile = consumption_per_one_km * MILE
    gallon_consumption_per_one_mile = consumption_per_one_mile / GALLON
    miles_per_gallon = 1 / gallon_consumption_per_one_mile

    return round(miles_per_gallon, 1)


fuel_consumption = []

with open('fuel_consumption.csv', newline='') as fuel_data:
    reader = csv.DictReader(fuel_data, delimiter=',', quotechar='|')
    fuel_consumption = [float(row['liters_per_100km']) for row in reader]

kilometer_str = "l/100km"
fuel_consumption_str = "fuel consumption is "
mpg_str = " miles/gallon"

print(f"Min {fuel_consumption_str} {min(fuel_consumption)}{kilometer_str} or {liter_per_kilometer_to_mpg(min(fuel_consumption))}{mpg_str}")
print(f"Max {fuel_consumption_str} {max(fuel_consumption)}{kilometer_str} or {liter_per_kilometer_to_mpg(max(fuel_consumption))}{mpg_str}")
print(f"Average {fuel_consumption_str} {statistics.median(fuel_consumption)}{kilometer_str} or {liter_per_kilometer_to_mpg(statistics.median(fuel_consumption))}{mpg_str}")
