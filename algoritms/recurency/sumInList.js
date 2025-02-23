// write a recursive function counting elements in the list

function sumInList(list) {
  if (list.length === 0) {
    return 0;
  } else {
    return list[0] + sumInList(list.slice(1));
  }
}

console.log(sumInList([2, 4, 6])); // 12