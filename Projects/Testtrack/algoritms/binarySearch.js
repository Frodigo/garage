// Step 1: Definition of the binarySearch function
function binarySearch(array, target) {
  // Step 2: Setting the initial indices left and right
  let left = 0;
  let right = array.length - 1;

  // Step 3: Loop until left exceeds right
  while (left <= right) {
    // Step 4: Calculating the middle index
    let mid = Math.floor((left + right) / 2);

    // Step 5: Checking if we found the target value
    if (array[mid] === target) {
      return mid; // Return the index if you find the value
    }

    // Step 6: Shifting the search range
    if (array[mid] < target) {
      // The target value is on the right side
      left = mid + 1;
    } else {
      // The target value is on the left side
      right = mid - 1;
    }
  }

  // Step 7: Return -1 if the element is not found
  return -1;
}

// Example usage:
const sortedArray = [1, 3, 5, 7, 9, 11, 13, 15];
const targetValue = 7;

const resultIndex = binarySearch(sortedArray, targetValue);

// Displaying the result
if (resultIndex !== -1) {
  console.log(`Element found at index: ${resultIndex}`);
} else {
  console.log(`Element not found in the array.`);
}
