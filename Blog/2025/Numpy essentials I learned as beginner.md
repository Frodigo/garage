---
title: NumPy Essentials
date: 2025-11-07
permalink: numpy-essentials-i-learned-as-a-beginner
---
I’m learning machine learning and I’m at level 0, just getting started. Last week, I was exploring things related to NumPy, and the result of my learning is a Jupyter notebook, which I wanted to share with you.

Note: You can find [Jupyter Notebook source here](https://github.com/Frodigo/garage/blob/main/Atlas/Engineering/machine-learning/level-0-python-and-math-essentials/numpy/numpy-essentials.ipynb) (On blog you can see this notebook converted to text).

NumPy (Numerical Python) is a Python library that makes working with numbers faster and easier. It offers new datatype: ndarray, vectorization and bunch of useful functions. NumPy is a tool that every ML or Data Engineer use daily.In this Notebook, I am going through NumPy features and show examples how it can be used.

## Installation

Run a cell below to install numpy:

```python
%pip install numpy
```

    Requirement already satisfied: numpy in /opt/anaconda3/envs/mlenv/lib/python3.13/site-packages (2.2.2)
    Note: you may need to restart the kernel to use updated packages.

Run this code to verify NumPy is installed:

```python
import numpy as np
print(np.__version__)
```

    2.2.2

You should see a version of NumPy.

**What this means:**

- `import numpy` - Load the NumPy library so you can use it
- `as np` - Create a nickname "np" so you can type `np.array()` instead of `numpy.array()` every time (we are lazy and we prefer to write to letters instead of five, yeah?)
- This is a convention - most NumPy code uses `np`, so you'll see it everywhere

**Why not just `import numpy`?** You can! But `np` is shorter and everyone uses it, so your code will match examples you find online. (and as i said, we are lazy, or at least me).

## NumPy Advantages

Once NumPy is installed, let's see it biggest advantages. Vectorization allows you to apply an operation to each element in array without doing a loop. Another thing is a bunch of methods that allows you to do mathematical operations. All of this will not be possible without a `ndarray`, which is a core data structure in NumPy.

### Vectorization

Vectorization allows applying an operation to an entire array at once, rather than looping through each element.

In NumPy, you can perform operations on entire arrays without explicit loops. For example `arr + 10` will add `10` to each element of `arr`.

Let's see this in action:

```python
import time  # Built-in Python module for measuring time

# Example: Converting engine RPM to different units
# Let's say we have RPM readings from a car's engine
rpm_values = [1000, 2000, 3000, 4000, 5000]

# Method 1: Using Python loop (slow way)
# Convert RPM to radians per second (multiply by 0.10472)
result_python = []
for rpm in rpm_values:
    result_python.append(rpm * 0.10472)
print(f"Using Python loop: {result_python}")

# Method 2: Using NumPy vectorization (fast way)
rpm_array = np.array(rpm_values)  # Convert list to NumPy array
result_numpy = rpm_array * 0.10472  # Single operation on entire array!
print(f"Using NumPy vectorization: {result_numpy}")
print("→ Same result, less code! This is called 'vectorization'")


```

    Using Python loop: [104.72, 209.44, 314.15999999999997, 418.88, 523.6]
    Using NumPy vectorization: [104.72 209.44 314.16 418.88 523.6 ]
    → Same result, less code! This is called 'vectorization'

In example above you can see that we can just do `rpm_array * 0.10472` and we don't need looping. That's great - less code, same results. But let's see how time consuming are these methods in large datasets. Imagine analyzing RPM data from 1 million readings. Spoiler: NumPy is way more faster!

```python
# Create large dataset: 1 million RPM values from 0 to 7000
# Note: range(1000000) creates numbers 0 to 999,999, then we multiply by 7
python_list = [rpm * 7 for rpm in range(1000000)]  # List comprehension
numpy_array = np.array(python_list)  # Convert to NumPy array

# Time the Python loop method
start = time.time()  # Record start time
result_python = []
for rpm in python_list:
    result_python.append(rpm * 0.10472)  # Convert each RPM
python_time = time.time() - start  # Calculate elapsed time

# Time the NumPy vectorization method
start = time.time()
result_numpy = numpy_array * 0.10472  # Single operation!
numpy_time = time.time() - start

print(f"Python loop time: {python_time:.4f} seconds")
print(f"NumPy vectorized time: {numpy_time:.4f} seconds")
print(f"NumPy is {python_time/numpy_time:.1f}x faster!")


```

    Python loop time: 0.0327 seconds
    NumPy vectorized time: 0.0008 seconds
    NumPy is 40.7x faster!

40x faster, amazing, no? Let's take a look at other vectorization examples:

```python

# Example: Processing speed data from GPS
speeds_mph = np.array([30, 45, 60, 70, 85])  # Speeds in mph
print(f"Original speeds (mph): {speeds_mph}")

# Convert to km/h (multiply by 1.60934)
speeds_kmh = speeds_mph * 1.60934
print(f"Converted to km/h: {speeds_kmh}")

# Calculate speeds in m/s (divide km/h by 3.6)
speeds_ms = speeds_kmh / 3.6
print(f"Converted to m/s: {speeds_ms}")

# Add 5 mph to all speeds (simulating cruise control adjustment)
adjusted_speeds = speeds_mph + 5
print(f"Adjusted speeds (+5 mph): {adjusted_speeds}")

# Calculate power (simplified: power ≈ speed²)
power = speeds_mph ** 2
print(f"Relative power (speed²): {power}")
```

    Original speeds (mph): [30 45 60 70 85]
    Converted to km/h: [ 48.2802  72.4203  96.5604 112.6538 136.7939]
    Converted to m/s: [13.41116667 20.11675    26.82233333 31.29272222 37.99830556]
    Adjusted speeds (+5 mph): [35 50 65 75 90]
    Relative power (speed²): [ 900 2025 3600 4900 7225]

### Mathematical Operations

NumPy offers built-in functions for linear algebra, statistics, and more. These are essential for analyzing automotive data - like calculating average fuel consumption, analyzing engine performance, or processing sensor readings.

Let's explore the most useful functions with automotive examples:

```python
# Example: Fuel consumption data (L/100km) from 10 different trips
fuel_consumption = np.array([7.2, 8.5, 6.9, 9.1, 7.8, 8.3, 7.5, 6.7, 8.9, 7.4])
print(f"Fuel consumption data (L/100km): {fuel_consumption}")
```

    Fuel consumption data (L/100km): [7.2 8.5 6.9 9.1 7.8 8.3 7.5 6.7 8.9 7.4]

#### Statistics

Based on our example we can easily analyze fuel consumption, calculating average speeds, finding performance metrics, or analyzing sensor data.

```python
print(f"Fuel consumption data (L/100km): {fuel_consumption}")
print(f"\nStatistics:")
print(f"Mean (average): {np.mean(fuel_consumption):.2f} L/100km")
print(f"Median (middle value): {np.median(fuel_consumption):.2f} L/100km")
print(f"Standard deviation (variability): {np.std(fuel_consumption):.2f} L/100km")
print(f"Variance: {np.var(fuel_consumption):.2f}")
print(f"Minimum: {np.min(fuel_consumption):.1f} L/100km (best efficiency)")
print(f"Maximum: {np.max(fuel_consumption):.1f} L/100km (worst efficiency)")
print(f"Range: {np.max(fuel_consumption) - np.min(fuel_consumption):.1f} L/100km")
print(f"50th percentile (median): {np.percentile(fuel_consumption, 50):.2f} L/100km")
```

    Fuel consumption data (L/100km): [7.2 8.5 6.9 9.1 7.8 8.3 7.5 6.7 8.9 7.4]

    Statistics:
    Mean (average): 7.83 L/100km
    Median (middle value): 7.65 L/100km
    Standard deviation (variability): 0.79 L/100km
    Variance: 0.63
    Minimum: 6.7 L/100km (best efficiency)
    Maximum: 9.1 L/100km (worst efficiency)
    Range: 2.4 L/100km
    50th percentile (median): 7.65 L/100km

#### Basic Math Operations

Simple but essential operations for automotive calculations.

```python
# Example: Engine RPM data
rpm = np.array([1000, 2000, 3000, 4000, 5000])
print(f"Engine RPM: {rpm}")

# Absolute value
rpm_diff = np.array([-100, 50, -200, 150, -75])
print(f"RPM differences: {rpm_diff}")
print(f"Absolute differences: {np.abs(rpm_diff)}")

# Square root
power = np.array([100, 200, 300, 400, 500])  # HP
print(f"\nPower (HP): {power}")
print(f"Square root of power: {np.sqrt(power)}")

# Exponentiation
speed = np.array([30, 40, 50, 60, 70])  # mph
print(f"\nSpeed (mph): {speed}")
print(f"Speed squared (used in power calculations): {speed ** 2}")
```

    Engine RPM: [1000 2000 3000 4000 5000]
    RPM differences: [-100   50 -200  150  -75]
    Absolute differences: [100  50 200 150  75]

    Power (HP): [100 200 300 400 500]
    Square root of power: [10.         14.14213562 17.32050808 20.         22.36067977]

    Speed (mph): [30 40 50 60 70]
    Speed squared (used in power calculations): [ 900 1600 2500 3600 4900]

#### Rounding & Precision

When working with data, you often need to round values for display or calculations.

```python
# Example: Precise fuel consumption readings
fuel_consumption = np.array([7.234, 8.567, 6.891, 9.123, 7.456])
print(f"Precise fuel consumption (L/100km): {fuel_consumption}")

# Round to 2 decimal places (typical for fuel consumption)
rounded = np.round(fuel_consumption, 2)
print(f"Rounded to 2 decimals: {rounded}")

# Round down (floor) - useful for conservative estimates
floored = np.floor(fuel_consumption)
print(f"Floored (rounded down): {floored}")

# Round up (ceiling) - useful for worst-case estimates
ceiled = np.ceil(fuel_consumption)
print(f"Ceiled (rounded up): {ceiled}")

# Example: Speed readings
speed = np.array([45.7, 62.3, 78.9, 91.2])
print(f"\nSpeed readings (mph): {speed}")
print(f"Rounded speeds: {np.round(speed)}")
```

    Precise fuel consumption (L/100km): [7.234 8.567 6.891 9.123 7.456]
    Rounded to 2 decimals: [7.23 8.57 6.89 9.12 7.46]
    Floored (rounded down): [7. 8. 6. 9. 7.]
    Ceiled (rounded up): [ 8.  9.  7. 10.  8.]

    Speed readings (mph): [45.7 62.3 78.9 91.2]
    Rounded speeds: [46. 62. 79. 91.]

## Understanding NumPy Arrays (ndarray)

`ndarray` is a core data structure in NumPy - a multidimensional array that can hold lots of data efficiently. Think of it as a supercharged Python list that's optimized for math.

**Key difference from Python lists:**

- Python lists can contain different data types (heterogeneous): `[1, "hello", 3.5]`
- NumPy arrays must contain the same data type (homogeneous): `[1, 2, 3]` or `[1.0, 2.0, 3.0]`

### Creating arrays

```python
my_arr = np.array([1, 2, 3, 4, 5])
my_arr.dtype

ones = np.ones((3, 4))
zeros = np.zeros((2, 3, 4))
full = np.full((2, 3), 4)
arange = np.arange(10, 100, 10)
linspace = np.linspace(0, 1, 5)

print(ones)
print(zeros)
print(full)
print(arange)
print(linspace)


random_arr = np.random.randint(0, 10, (3, 4))
print(random_arr)

random_arr_2 = np.random.rand(2, 2, 2, 2)
print(random_arr_2)

```

    [[1. 1. 1. 1.]
     [1. 1. 1. 1.]
     [1. 1. 1. 1.]]
    [[[0. 0. 0. 0.]
      [0. 0. 0. 0.]
      [0. 0. 0. 0.]]

     [[0. 0. 0. 0.]
      [0. 0. 0. 0.]
      [0. 0. 0. 0.]]]
    [[4 4 4]
     [4 4 4]]
    [10 20 30 40 50 60 70 80 90]
    [0.   0.25 0.5  0.75 1.  ]
    [[6 1 8 4]
     [1 7 3 9]
     [8 3 1 4]]
    [[[[0.59130761 0.66421588]
       [0.33191183 0.29026851]]

      [[0.39059243 0.12892054]
       [0.01739604 0.80804896]]]


     [[[0.32469533 0.29820351]
       [0.21903883 0.53010489]]

      [[0.53026239 0.05754576]
       [0.31187082 0.55165342]]]]

#### Array Properties

Understanding array properties helps you work with your data effectively.

```python
# Example: Engine sensor data
sensor_data = np.array([[30, 2500, 7.2],   # [speed, RPM, fuel]
                        [45, 3000, 8.5],
                        [60, 3500, 9.1]])

print(f"Array:\n{sensor_data}")
print(f"\nArray Properties:")
print(f".shape → {sensor_data.shape} (rows, columns)")
print(f".ndim → {sensor_data.ndim} (number of dimensions)")
print(f".size → {sensor_data.size} (total elements)")
print(f".dtype → {sensor_data.dtype} (data type)")
print(f".itemsize → {sensor_data.itemsize} bytes per element")
print(f".nbytes → {sensor_data.nbytes} bytes total")

# Example: 1D array
speed_data = np.array([30, 45, 60, 70, 85])
print(f"\n1D array: {speed_data}")
print(f"Shape: {speed_data.shape} (note the comma - it's a tuple!)")
print(f"Dimensions: {speed_data.ndim}D")
```

    Array:
    [[  30.  2500.     7.2]
     [  45.  3000.     8.5]
     [  60.  3500.     9.1]]

    Array Properties:
    .shape → (3, 3) (rows, columns)
    .ndim → 2 (number of dimensions)
    .size → 9 (total elements)
    .dtype → float64 (data type)
    .itemsize → 8 bytes per element
    .nbytes → 72 bytes total

    1D array: [30 45 60 70 85]
    Shape: (5,) (note the comma - it's a tuple!)
    Dimensions: 1D

Array properties help you understand your data. `.shape` shows the structure of the array and it's helpful to check if the data format is correct. `.dtype` indicates what type of data is stored in the array. `.nbytes` displays how much memory the array uses (critical when working with very large arrays).

### ndarray (n-dimensional array)

`ndarray` is multidimensional array that can be 0D (scalar), 1D (vector), 2D (matrix), or higher dimensions. Let's take a look at examples.

#### 0D Array (scalar)

```python
scalar = np.array(42)
print(f"Array: {scalar}")
print(f"Shape: {scalar.shape}")
print(f"Dimensions: {scalar.ndim}D")
print(f"Data type: {scalar.dtype}")
print(f"Size: {scalar.size}")
```

    Array: 42
    Shape: ()
    Dimensions: 0D
    Data type: int64
    Size: 1

#### 1D array (vector)

```python
vector = np.array([1, 2, 3, 4, 5])
print(f"Array: {vector}")
print(f"Shape: {vector.shape}")
print(f"Dimensions: {vector.ndim}D")
print(f"Data type: {vector.dtype}")
print(f"Size: {vector.size}")
```

    Array: [1 2 3 4 5]
    Shape: (5,)
    Dimensions: 1D
    Data type: int64
    Size: 5

#### 2D array (matrix)

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"Array:\n{matrix}")
print(f"Shape: {matrix.shape} (rows, columns)")
print(f"Dimensions: {matrix.ndim}D")
print(f"Data type: {matrix.dtype}")
print(f"Size: {matrix.size} (total elements)")
```

    Array:
    [[1 2 3]
     [4 5 6]
     [7 8 9]]
    Shape: (3, 3) (rows, columns)
    Dimensions: 2D
    Data type: int64
    Size: 9 (total elements)

#### 3D array

```python
array_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(f"Array:\n{array_3d}")
print(f"Shape: {array_3d.shape} (depth, rows, columns)")
print(f"Dimensions: {array_3d.ndim}D")
print(f"Data type: {array_3d.dtype}")
print(f"Size: {array_3d.size} (total elements)")
```

    Array:
    [[[1 2]
      [3 4]]

     [[5 6]
      [7 8]]]
    Shape: (2, 2, 2) (depth, rows, columns)
    Dimensions: 3D
    Data type: int64
    Size: 8 (total elements)

#### Creating array from list

```python
list_1d = [1, 2, 3, 4, 5]
list_2d = [[1, 2, 3], [4, 5, 6]]
arr_from_list_1d = np.array(list_1d)
arr_from_list_2d = np.array(list_2d)
print(f"1D list {list_1d} → Array: {arr_from_list_1d}")
print(f"2D list {list_2d} → Array:\n{arr_from_list_2d}")
```

    1D list [1, 2, 3, 4, 5] → Array: [1 2 3 4 5]
    2D list [[1, 2, 3], [4, 5, 6]] → Array:
    [[1 2 3]
     [4 5 6]]

#### Homogenous data type

`ndarray` stores the same data type. If needed types will be converted.

```python
mixed_list = [1, 2, 3.5, 4]  # Mix of int and float
homogeneous_array = np.array(mixed_list)
print(f"Mixed list: {mixed_list}")
print(f"NumPy array: {homogeneous_array}")
print(f"Data type: {homogeneous_array.dtype} (all converted to float)")
```

    Mixed list: [1, 2, 3.5, 4]
    NumPy array: [1.  2.  3.5 4. ]
    Data type: float64 (all converted to float)

### Broadcasting

**What is broadcasting?** NumPy allows using arrays of different shapes in arithmetic operations thanks to broadcasting rules, which automatically handle shape mismatches. Broadcasting is a powerful mechanism that lets NumPy work with arrays of different shapes when performing operations, making code more concise and readable.

Let's see this in action with automotive examples:

#### Example 1: Adding a calibration offset to all speed readings

```python
import numpy as np

# Speed readings from GPS (mph) - 2D array with multiple trips
speeds = np.array([[30, 45, 60],
                   [40, 55, 70],
                   [35, 50, 65]])

# Calibration offset: GPS is reading 2 mph too low
calibration_offset = 2

print(f"Speed readings (mph):\n{speeds}")
print(f"\nCalibration offset: +{calibration_offset} mph")
print(f"\nAdjusted speeds:\n{speeds + calibration_offset}")
print("→ The scalar (2) is 'broadcast' to every element!")
```

    Speed readings (mph):
    [[30 45 60]
     [40 55 70]
     [35 50 65]]

    Calibration offset: +2 mph

    Adjusted speeds:
    [[32 47 62]
     [42 57 72]
     [37 52 67]]
    → The scalar (2) is 'broadcast' to every element!

#### Example 2: Applying different adjustments per column

```python
speeds = np.array([[30, 45, 60],
                   [40, 55, 70],
                   [35, 50, 65]])

# Different calibration offsets
trip_adjustments = np.array([2, 3, 1])

print(f"Speed readings (mph):\n{speeds}")
print(f"\nTrip adjustments: {trip_adjustments}")
print(f"\nAdjusted speeds:\n{speeds + trip_adjustments}")
```

    Speed readings (mph):
    [[30 45 60]
     [40 55 70]
     [35 50 65]]

    Trip adjustments: [2 3 1]

    Adjusted speeds:
    [[32 48 61]
     [42 58 71]
     [37 53 66]]

#### Example 3: Applying adjustments per row

```python
speeds = np.array([[30, 45, 60],
                   [40, 55, 70]])

time_adjustments = np.array([[1],
                             [2]])

print(f"Speed readings (mph):\n{speeds}")
print(f"\nTime-based adjustments (column vector):\n{time_adjustments}")
print(f"\nAdjusted speeds:\n{speeds + time_adjustments}")
```

    Speed readings (mph):
    [[30 45 60]
     [40 55 70]]

    Time-based adjustments (column vector):
    [[1]
     [2]]

    Adjusted speeds:
    [[31 46 61]
     [42 57 72]]

### Random Number Generation

NumPy provides functions for generating random numbers, probability distributions, and random sampling.

```python
# Simulate random speed readings (mph)
speeds = np.random.randint(30, 90, size=10)  # Random speeds between 30-90 mph
print(f"Random speeds (mph): {speeds}")

```

    Random speeds (mph): [53 82 65 69 53 32 51 82 31 53]

```python
# Simulate speed readings with realistic distribution
realistic_speeds = np.random.normal(loc=60, scale=15, size=10)  # Mean 60, std 15
print(f"\nRealistic speeds (normal distribution): {realistic_speeds}")
print(f"Mean: {realistic_speeds.mean():.1f} mph, Std: {realistic_speeds.std():.1f} mph")

```

    Realistic speeds (normal distribution): [52.95788421 68.13840065 53.04873461 53.0140537  63.62943407 31.30079633
     34.12623251 51.56568706 44.80753319 64.71370999]
    Mean: 51.7 mph, Std: 11.7 mph

```python
# Simulate fuel consumption (L/100km) - uniform distribution
fuel_consumption = np.random.uniform(low=6.0, high=10.0, size=5)
print(f"Simulated fuel consumption (L/100km): {fuel_consumption}")
print(f"Average: {fuel_consumption.mean():.2f} L/100km")

```

    Simulated fuel consumption (L/100km): [7.16857859 7.46544737 7.82427994 9.14070385 6.79869513]
    Average: 7.68 L/100km

```python
# Simulate RPM readings (1000-7000 RPM)
rpm_readings = np.random.randint(1000, 7000, size=5)
print(f"Random RPM readings: {rpm_readings}")

```

    Random RPM readings: [6390 6226 6191 4772 4092]

```python
# Simulate RPM with normal distribution (typical cruising RPM)
cruising_rpm = np.random.normal(loc=2500, scale=500, size=5)
print(f"\nCruising RPM (normal distribution): {cruising_rpm}")
print(f"Mean: {cruising_rpm.mean():.0f} RPM")

```

    Cruising RPM (normal distribution): [2382.92331264 2382.93152153 3289.60640775 2883.71736458 2265.26280703]
    Mean: 2641 RPM

```python
# Simulate selecting random trips for analysis
trip_ids = ['Trip 1', 'Trip 2', 'Trip 3', 'Trip 4', 'Trip 5']
selected_trips = np.random.choice(trip_ids, size=3, replace=False)
print(f"Available trips: {trip_ids}")
print(f"Randomly selected trips: {selected_trips}")

```

    Available trips: ['Trip 1', 'Trip 2', 'Trip 3', 'Trip 4', 'Trip 5']
    Randomly selected trips: ['Trip 3' 'Trip 2' 'Trip 5']

```python
print("Setting seed ensures reproducible results (important for testing!):")
np.random.seed(42)
speed1 = np.random.randint(30, 90, size=3)
print(f"With seed(42): {speed1}")

np.random.seed(42)
speed2 = np.random.randint(30, 90, size=3)
print(f"With seed(42) again: {speed2}")
print("→ Same seed produces same random numbers!")

```

    Setting seed ensures reproducible results (important for testing!):
    With seed(42): [68 81 58]
    With seed(42) again: [68 81 58]
    → Same seed produces same random numbers!

---

## Common Mistakes

Here are some common mistakes beginners make when starting with NumPy:

### Mistake 1: Forgetting to convert to NumPy array

```python
my_list = [10, 20, 30]
print(f"Python list: {my_list}")
print(f"my_list * 2 → {my_list * 2}")  # Duplicates the list!
print("⚠️ Python lists multiply by duplicating, not by element!")

my_array = np.array([10, 20, 30])
print(f"\nNumPy array: {my_array}")
print(f"my_array * 2 → {my_array * 2}")  # Multiplies each element!
print("✅ NumPy arrays multiply each element")

```

    Python list: [10, 20, 30]
    my_list * 2 → [10, 20, 30, 10, 20, 30]
    ⚠️ Python lists multiply by duplicating, not by element!

    NumPy array: [10 20 30]
    my_array * 2 → [20 40 60]
    ✅ NumPy arrays multiply each element

### Mistake 2: Mixing up array dimensions

```python
# 1D array (like a row of data)
array_1d = np.array([10, 20, 30])
print(f"1D array: {array_1d}")
print(f"Shape: {array_1d.shape}")

# 2D array with 1 row
array_2d_row = np.array([[10, 20, 30]])
print(f"\n2D array with 1 row: {array_2d_row}")
print(f"Shape: {array_2d_row.shape}")

# 2D array with 1 column
array_2d_col = np.array([[10], [20], [30]])
print(f"\n2D array with 1 column:\n{array_2d_col}")
print(f"Shape: {array_2d_col.shape}")

```

    1D array: [10 20 30]
    Shape: (3,)

    2D array with 1 row: [[10 20 30]]
    Shape: (1, 3)

    2D array with 1 column:
    [[10]
     [20]
     [30]]
    Shape: (3, 1)

# Mistake 3: Not understanding data type

```python
# Mixing integers and floats
mixed_list = [10, 20, 30.5, 40]
print(f"Mixed list: {mixed_list}")
mixed_array = np.array(mixed_list)
print(f"NumPy array: {mixed_array}")
print(f"Data type: {mixed_array.dtype}")
print("⚠️ NumPy converts all to same type (float in this case)")

# All integers stay integers
int_list = [10, 20, 30, 40]
int_array = np.array(int_list)
print(f"\nInteger list: {int_list}")
print(f"NumPy array: {int_array}")
print(f"Data type: {int_array.dtype}")
print("✅ All integers stay integers")
```

    Mixed list: [10, 20, 30.5, 40]
    NumPy array: [10.  20.  30.5 40. ]
    Data type: float64
    ⚠️ NumPy converts all to same type (float in this case)

    Integer list: [10, 20, 30, 40]
    NumPy array: [10 20 30 40]
    Data type: int64
    ✅ All integers stay integers

## Summary

In this notebook, we've covered some essential and practical aspects of using NumPy in Python:

- How to create arrays and the differences between Python lists and NumPy arrays
- Common mistakes, including operating on Python lists vs NumPy arrays, mixing data types, and misunderstanding array shapes/dimensions
- Useful attributes such as `.shape` and `.dtype`
- Conversion between 1D and 2D arrays and understanding reshape behavior

I spent approximatelly 1 hour every day in a week to learn, play, expermiment and write this notebook. If I did it, you can too!

## Topics for Further Learning

If you wish to deepen your NumPy skills, consider exploring the following:

- NumPy array broadcasting rules and how they apply to arithmetic operations
- Advanced indexing and slicing techniques (fancy indexing, boolean indexing)
- Vectorized computations for performance improvements
- Useful NumPy functions: `np.dot`, `np.linalg`, `np.random`
- Memory layout and the difference between `np.copy()` and view/reference semantics
- Integrating NumPy with pandas and plotting libraries like matplotlib
- Working with higher-dimensional arrays and practical applications in scientific computing
