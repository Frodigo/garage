import math


def binary_search(arr: list, target: int) -> int:
    """
    Performs binary search on a sorted array to find the target value.

    Args:
        arr (list): A sorted list of elements to search through.
        target (int): The value to search for in the array.

    Returns:
        int: The index of the target element if found, -1 otherwise.

    Time Complexity:
        O(log n) where n is the length of the array.
    """
    left_index = 0
    right_index = len(arr) - 1

    while (left_index <= right_index):
        mid = math.floor((left_index + right_index) / 2)

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left_index = mid + 1
        else:
            right_index = mid - 1

    return -1


if __name__ == "__main__":
    sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]
    target_value = 7

    print(binary_search(sorted_list, target_value))
