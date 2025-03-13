function sumInArray(array) {
  if (array.length === 0) {
    return 0;
  } else if (array.length === 1) {
    return array[0];
  }

  return array[0] + sumInArray(array.slice(1));
}

console.log(sumInArray([2,4,6])); 