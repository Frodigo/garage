# Basic Python programs

1. [Fuel-consumption analysis](./fuel-consumption-analysis/README.md)
2. [Engine-power conversion](./engine‑power-conversion/README.md)

---

## 3. Filtering a car list by CO₂ emissions

- **Description:** You have a list of car models and their CO₂ emissions (g/km). Write a program that:

  1. Reads data such as `[("ModelA", 120), ("ModelB", 95), ("ModelC", 140), …]`.
  2. Allows the user to enter a maximum permitted emission value (e.g., 100 g/km).
  3. Returns a list of models that do not exceed this value.

- **Extension:** Sort the results ascending by emissions or add a second criterion (e.g., engine power).

---

## 4. Reading engine‑temperature logs

- **Description:** You have a file `engine_temps.txt` that stores engine temperatures (°C) every 10 seconds, one temperature per line.
  - Write a program that:
    1. Reads the entire file.
    2. Counts and displays:
       - the number of entries (how many measurements),
       - the average temperature,
       - the highest and lowest recorded temperatures.
  - **Extension:** Show a warning if the highest temperature exceeds a set threshold (e.g., 120 °C).

---

## 5. Dictionary of car‑model information

- **Description:** Create a dictionary in which the keys are car‑model names and the values are dictionaries with additional info, e.g.:

  ```python
  {
      "ModelX": {"power": 150, "engine_capacity": 1.8, "fuel_type": "petrol"},
      "ModelY": {"power": 110, "engine_capacity": 1.6, "fuel_type": "diesel"}
  }
  ```

  - Write a function that takes such a dictionary and:
    1. Displays all available models.
    2. Lets the user choose one model and returns its details.

- **Extension:** Allow adding new models and saving them to a JSON file.

---

## 6. Calculating motorway‑toll cost

- **Description:** Imagine you have a table of motorway tolls that depend on trip length and vehicle category (e.g., `car`, `motorcycle`, `truck`).
  - Write a program that:
    1. Accepts the trip length (km).
    2. Allows the user to choose a vehicle category.
    3. Calculates and shows the estimated toll cost.
  - **Extension:**
    - If the cost exceeds 100 PLN, suggest a discount or an alternative route.
    - Add currency handling (PLN, EUR).

---

## 7. Insurance‑class calculation

- **Description:** Assume that an insurance premium depends on:

  - Owner’s age
  - Engine capacity
  - Claim‑free history (years without accidents)
  - Place of residence
  - etc.
  - Write a program that asks the user for these data (or reads them from a file) and then calculates an approximate insurance premium based on a few simple formulas.

- **Extension:** Use conditional statements (`if`) so that different age or engine‑capacity ranges apply different multipliers.

---

## 8. Gear‑shift simulation

- **Description:** Write a function that simulates gear changes in a car, taking the current speed as a parameter. Assume speed thresholds (e.g., 0–20 km/h → 1st gear, 21–40 → 2nd, etc.).
  - Depending on the input speed, the function returns which gear should be engaged.
  - **Extension:** Add support for manual and automatic transmissions (e.g., different shift points).

---

## 9. Trip analysis (GPS log)

- **Description:** Assume you have a list (or a CSV file) with sequential GPS points from a trip (e.g., every minute) and the speed at each point.
  - Write a program that calculates:
    1. The total trip length (approximate, based on distances between GPS points).
    2. The average speed.
    3. The maximum speed.
  - **Extension:** Use the haversine formula to compute distances from geographic coordinates.

---

## 10. Fleet‑analysis statistics

- **Description:** Imagine a company owns a fleet of several dozen vehicles. For each vehicle you store, for example:
  - Year of manufacture
  - Mileage (km)
  - VIN
  - Make, Model
  - Date of last inspection
  - Write a program that:
    1. Reads these data from a file (CSV or JSON).
    2. Calculates and prints:
       - Average mileage of the fleet,
       - Oldest and newest model year,
       - Number of days since the last inspection for each vehicle (assuming the current date).
  - **Extension:** Group vehicles by make or model year and compute statistics within those groups.

---
