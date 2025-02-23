function quickSort(array) {
    // Stop condition: if the array has less than 2 elements, no need to sort
    if (array.length < 2) {
      return array;
    }
  
    // Choosing the pivot (here we choose the middle element)
    const pivotIndex = Math.floor(array.length / 2);
    const pivot = array[pivotIndex];
  
    // Arrays to store elements smaller and larger than the pivot
    let left = [];
    let right = [];
  
    // We go through all elements (except the pivot) and divide the array
    for (let i = 0; i < array.length; i++) {
      if (i === pivotIndex) continue; // Skip the pivot
  
      if (array[i] < pivot) {
        left.push(array[i]);
      } else {
        right.push(array[i]);
      }
    }
  
    // Recursive call for the left and right parts and combining the results
    return [...quickSort(left), pivot, ...quickSort(right)];
  }
  
  // Example usage:
  const array = [3, 6, 8, 10, 1, 2, 123, 2, 26, 1];
  console.log(quickSort(array));  // [1, 1, 2, 2, 3, 6, 8, 10, 26, 123]
  