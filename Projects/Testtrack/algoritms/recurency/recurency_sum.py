def sum_in_array(arr: list) -> int:
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        return arr[0]
    else:
        return arr[0] + sum_in_array(arr[1:])


if __name__ == "__main__":
    print(sum_in_array([2, 4, 6]))
