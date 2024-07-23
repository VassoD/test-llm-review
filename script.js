function findLargestNumber(arr) {
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

function calculateAverage(nums) {
  var sum = 0;
  for (var i = 0; i < nums.length; i++) {
    sum += nums[i];
  }
  return sum / nums.length;
}

var result1 = findLargestNumber(numbers);
var result2 = calculateAverage(numbers);
console.log("Largest:", result1);
console.log("Average:", result2);
