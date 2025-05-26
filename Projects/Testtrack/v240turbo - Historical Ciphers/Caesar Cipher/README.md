### Caesar Cipher

The Caesar cipher is one of the earliest and simplest encryption techniques. It was used by Julius Caesar for his private correspondence.

It works by shifting each letter in the plaintext by a fixed number of positions in the alphabet.

Key features:

- Encrypt text using a specified shift value
- Decrypt text using the same shift value
- Preserve case (uppercase/lowercase) during encryption/decryption
- Handle wraparound at alphabet boundaries (Z → A)
- Preserve non-alphabetic characters (spaces, numbers, punctuation)
- Support for negative shift values

## How Caesar Cipher Works

### Encryption Process

1. Take each letter in the plaintext message
2. Shift it forward in the alphabet by the specified amount (the key)
3. Wrap around from Z to A if necessary
4. Non-alphabetic characters remain unchanged

Example with a shift of 3:

- A → D
- B → E
- C → F
- ...
- Z → C

### Decryption Process

1. Take each letter in the encrypted message
2. Shift it backward in the alphabet by the same amount
3. Wrap around from A to Z if necessary
4. Non-alphabetic characters remain unchanged
