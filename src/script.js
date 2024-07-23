function findLargestNumber(arr) {
  arr = arr.map(Number);
  let largest = arr[0];
  for (let i = 1; i < arr.length; i++) {
    if (arr[i] > largest) {
      largest = arr[i];
    }
  }
  return largest;
}
let numbers = [3, 5, 7, 2, 8];

console.log(findLargestNumber(numbers));
