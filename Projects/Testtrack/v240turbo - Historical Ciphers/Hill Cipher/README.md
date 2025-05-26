### Hill Cipher

The Hill cipher is a polygraphic substitution cipher based on linear algebra. It was invented by Lester S. Hill in 1929 and was the first polygraphic cipher that was practical to operate on more than three symbols at once.

Key features:

- Uses matrix multiplication for encryption and decryption
- Supports 1x1, 2x2, and 3x3 matrices
- Processes text in blocks equal to the matrix size
- Automatically pads text to match block size
- More secure than simple substitution ciphers
- Resistant to frequency analysis

## How Hill Cipher Works

### Encryption Process

1. Convert the plaintext to numbers (A=0, B=1, ..., Z=25)
2. Arrange the numbers in blocks matching the matrix size
3. Multiply each block by the encryption matrix
4. Take the result modulo 26
5. Convert back to letters

### Decryption Process

1. Calculate the inverse of the encryption matrix modulo 26
2. Convert ciphertext to numbers
3. Arrange in blocks matching the matrix size
4. Multiply each block by the inverse matrix
5. Take the result modulo 26
6. Convert back to letters

### Matrix Input Format

When using the Hill cipher in the program:

1. Enter the matrix size (1, 2, or 3)
2. Enter each row of the matrix on a separate line
3. Numbers should be space-separated

Example for 2x2 matrix:

```shell
Row 1: 3 2
Row 2: 5 7
```
