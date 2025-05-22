import csv

with open('fuel_consumption.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in reader:
        print(', '.join(row))
