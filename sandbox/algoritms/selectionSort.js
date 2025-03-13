function findSmallest(arr) {
  let smallest = arr[0];
  let smallestIndex = 0;

  for (let i = 1; i < arr.length; i++) {
    if (arr[i] < smallest) {
      smallest = arr[i];
      smallestIndex = i;
    }
  }

  return smallestIndex;
}


function selectionSort(arr) {
    let newArr = [];
    
    // While there are elements in the array arr
    while (arr.length > 0) {
      // Find the index of the smallest element
      let smallest = findSmallest(arr);
      // Remove the smallest element and add it to newArr
      newArr.push(arr.splice(smallest, 1)[0]);
    }
  
    return newArr;
  }

console.log(selectionSort([5, 3, 6, 2, 10])); // [2, 3, 5, 6, 10]
