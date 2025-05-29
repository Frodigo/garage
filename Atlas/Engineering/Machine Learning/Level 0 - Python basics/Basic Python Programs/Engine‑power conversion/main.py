print("Engine power conversion!")

unit: str = input("From which unit do you want to convert? HP or kW?").lower()

while unit not in ["hp", "kw"]:
    unit = input(
        "Please choose one of two possible values: 'hp' or 'kw':").lower()


number = None

while number is None:
    try:
        number = float(input("Please provide a value you want to convert: "))
        if number < 0:
            print("Please enter a positive number")
            number = None
    except ValueError:
        print("Invalid input, please enter a valid number")

HP_TO_KW = 0.7355  # 1 HP = 0.7355 kW

if unit == "hp":
    result = round(number * HP_TO_KW, 2)
    print(f"{number} HP equals {result} kW")
else:
    result = round(number / HP_TO_KW, 2)
    print(f"{number} kW = {result} HP")

print("Conversion completed successfully!")
