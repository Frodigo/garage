### Vigenère Cipher

The Vigenère cipher is a polyalphabetic substitution cipher that uses a keyword to determine shifting. It was first described by Giovan Battista Bellaso in 1553, but misattributed to Blaise de Vigenère in the 19th century.

It improves upon the Caesar cipher by using different shift values for each letter in the plaintext, making it more resistant to frequency analysis.

Key features:

- Uses a keyword to determine the shift value for each letter
- Cycles through the keyword for longer messages
- Preserves case (uppercase/lowercase) during encryption/decryption
- Preserves non-alphabetic characters (spaces, numbers, punctuation)
- More secure than simple substitution ciphers

## How Vigenère Cipher Works

### Encryption Process

1. Take a keyword (e.g., "KEY")
2. For each letter in the plaintext:
   - Use the corresponding letter in the keyword to determine the shift
   - A = 0, B = 1, C = 2, ... , Z = 25
   - Cycle through the keyword for messages longer than the key
3. Apply the shift to the plaintext letter
4. Non-alphabetic characters remain unchanged

Example with keyword "KEY":

- K = shift by 10
- E = shift by 4
- Y = shift by 24
- (repeat for longer messages)

For plaintext "HELLO":

- H + K = R (shift H by 10)
- E + E = I (shift E by 4)
- L + Y = J (shift L by 24)
- L + K = V (shift L by 10)
- O + E = S (shift O by 4)

Resulting in ciphertext "RIJVS"

### Decryption Process

1. Use the same keyword as for encryption
2. For each letter in the ciphertext:
   - Use the corresponding letter in the keyword to determine the reverse shift
   - Subtract the shift value (with appropriate modulo arithmetic)
3. Non-alphabetic characters remain unchanged
