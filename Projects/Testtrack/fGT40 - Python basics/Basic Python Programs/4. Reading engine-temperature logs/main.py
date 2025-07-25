from functools import reduce

with open("engine_temps.txt", "r", encoding="utf-8") as file:
    MAX_TEMPERATURE_THRESHOLD = 120
    temperatures = [float(line.strip()) for line in file]
    meauserements_count = len(temperatures)
    average_temp = reduce(lambda acc, temperature: acc +
                          temperature, temperatures, 0) / meauserements_count
    max_temperature = max(temperatures)
    min_temperature = min(temperatures)

    print(f"{meauserements_count} entries in the file.")
    print(f"The average temperature is {round(average_temp, 2)} °C")
    print(f"Max temperature is {round(max_temperature, 2)} °C")
    print(f"Min temperature is {round(min_temperature, 2)} °C")

    if max_temperature > MAX_TEMPERATURE_THRESHOLD:
        print("ALERT: max temperature exceeds allowed max temperature for this engine!")
