// find the largest number in the list

function maxInList(list) {
  if (list.length === 0) {
    return null;
  } else if (list.length === 1) {
    return list[0];
  } else {
    let max = list[0];
    let rest = maxInList(list.slice(1));
    return max > rest ? max : rest;
  }
}

console.log(maxInList([2, 4, 100, 3, 6])); // 6
