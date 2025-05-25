def max_in_list(arr: list) -> int:
    if len(arr) == 0:
        return None
    elif len(arr) == 1:
        return arr[0]
    else:
        max = arr[0]
        rest = max_in_list(arr[1:])

        return max if max > rest else rest


if __name__ == "__main__":
    print(max_in_list([2, 3, 100, 3, 12, 25, 101, 32]))
