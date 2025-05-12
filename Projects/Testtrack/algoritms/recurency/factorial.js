function factorial(n) {
  // Stop condition
  if (n === 0 || n === 1) {
    return 1;
  }
  // Recursive call
  return n * factorial(n - 1);
}

// Example usage:
console.log(factorial(5)); // Result: 120
