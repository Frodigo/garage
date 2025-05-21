def quick_sort(arr: list) -> list:
    """
    Performs quick sort algorithm on a list of elements.

    Args:
        arr (list): The list of elements to be sorted.

    Returns:
        list: A new sorted list containing the same elements.

    Time Complexity:
        Average case: O(n log n)
        Worst case: O(n²) when the list is already sorted
    """
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]

        less = [i for i in arr[1:] if i <= pivot]
        greater = [i for i in arr[1:] if i > pivot]

        return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == '__main__':
    print(quick_sort([12, 1, 4215, 2, 45, 28, 83, 23, 621]))
