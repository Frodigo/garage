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

## Project Structure

- `Program.cs`: Main entry point and console interface
- `Ciphers/`: Contains the cipher implementations and interfaces
  - `ICipher.cs`: Common interface for all cipher implementations
  - `CipherFactory.cs`: Factory for creating and managing cipher implementations
  - `Caesar/`: Caesar cipher implementation

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
