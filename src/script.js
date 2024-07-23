/**
 * Finds the largest number in an array of numbers.
 * @param {number[]} numbersArray - The array of numbers to search.
 * @returns {number} The largest number in the array.
 * @throws {Error} If the input is not an array or if the array is empty.
 */
const findLargestNumber = (numbersArray = []) => {
  if (!Array.isArray(numbersArray) || numbersArray.length === 0) {
    throw new Error("Input must be a non-empty array of numbers");
  }
  return Math.max(...numbersArray);
};

/**
 * Calculates the average of an array of numbers.
 * @param {number[]} numbersArray - The array of numbers to average.
 * @returns {number} The average of the numbers in the array.
 * @throws {Error} If the input is not an array or if the array is empty.
 */
const calculateAverage = (numbersArray = []) => {
  if (!Array.isArray(numbersArray) || numbersArray.length === 0) {
    throw new Error("Input must be a non-empty array of numbers");
  }
  return numbersArray.reduce((sum, num) => sum + num, 0) / numbersArray.length;
};

// Example usage
const numbers = [3, 5, 7, 2, 8];
const largest = findLargestNumber(numbers);
const average = calculateAverage(numbers);

console.log("Largest:", largest);
console.log("Average:", average);
