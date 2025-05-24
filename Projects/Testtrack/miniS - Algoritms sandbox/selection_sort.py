def _find_smallest(arr: list):
    if not arr:
        return None

    smallest = arr[0]
    smallest_index = 0

    for i, j in enumerate(arr):
        if (j < smallest):
            smallest = j
            smallest_index = i

    return smallest_index


def selection_sort(arr: list):
    new_arr = []
    arr_copy = arr.copy()

    while (len(arr_copy) > 0):
        smallest = _find_smallest(arr_copy)
        new_arr.append(arr_copy.pop(smallest))

    return new_arr


if __name__ == "__main__":
    print(selection_sort([5, 3, 6, 2, 10]))
