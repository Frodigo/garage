# Historical Ciphers Demo

A C# implementation and interactive demo of historical encryption techniques.

## Overview

This project demonstrates various historical encryption techniques, starting with the Caesar cipher.

## Features

- Encrypt and decrypt text using various historical ciphers
- Interactive console application with user-friendly menus
- Extendable architecture for adding more cipher implementations
- Comprehensive test suite using xUnit

## Available Ciphers

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

## Project Structure

- `Program.cs`: Main entry point and console interface
- `Ciphers/`: Contains the cipher implementations and interfaces
  - `ICipher.cs`: Common interface for all cipher implementations
  - `CipherFactory.cs`: Factory for creating and managing cipher implementations
  - `Caesar/`: Caesar cipher implementation
  - `Vigenère/`: Vigenère cipher implementation

## Testing

The project follows Test-Driven Development (TDD) principles.

To run the tests:

```shell
dotnet test
```

## Building and Running

### Prerequisites

- .NET 9.0 or later

### Build

```shell
dotnet build
```

### Run

```shell
dotnet run
```

## Adding New Ciphers

To add a new cipher:

1. Create a new class that implements the `ICipher` interface
2. Register the cipher in `Program.cs` using the `CipherFactory`

Example:

```csharp
// Register ciphers
_cipherFactory.RegisterCipher(new CaesarCipher());
_cipherFactory.RegisterCipher(new YourNewCipher());
```

## License

[MIT License](LICENSE)

## Acknowledgments

- This project was developed as a learning exercise for basic cryptography concepts
- Implementation follows strict TDD (Test-Driven Development) principles
