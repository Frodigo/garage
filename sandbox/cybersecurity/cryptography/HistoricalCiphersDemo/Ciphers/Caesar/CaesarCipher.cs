using System.Text;

namespace HistoricalCiphersDemo.Ciphers.Caesar;

/// <summary>
/// Implementation of the Caesar cipher
/// </summary>
public class CaesarCipher : ICipher
{
    /// <summary>
    /// Gets the name of the cipher
    /// </summary>
    public string Name => "Caesar Cipher";

    /// <summary>
    /// Gets a description of how the cipher works
    /// </summary>
    public string Description => "The Caesar cipher is one of the earliest and simplest encryption techniques. " +
                                 "It works by shifting each letter in the plaintext by a fixed number of positions in the alphabet.";

    /// <summary>
    /// Encrypts the given text using the Caesar cipher
    /// </summary>
    /// <param name="text">The text to encrypt</param>
    /// <param name="key">The shift value (must be convertible to int)</param>
    /// <returns>The encrypted text</returns>
    public string Encrypt(string text, object key)
    {
        if (string.IsNullOrEmpty(text))
            return string.Empty;

        if (key is not int shift)
        {
            try
            {
                shift = Convert.ToInt32(key);
            }
            catch
            {
                throw new ArgumentException("Key must be convertible to an integer for Caesar cipher", nameof(key));
            }
        }

        var result = new StringBuilder();

        foreach (char inputChar in text)
        {
            // Check if character is a letter
            if (char.IsLetter(inputChar))
            {
                bool isLower = char.IsLower(inputChar);
                char baseChar = isLower ? 'a' : 'A';

                // Normalize to 0-25 range, apply shift, handle wrap-around
                int normalizedChar = (inputChar - baseChar + shift) % 26;
                // Handle negative modulo results
                if (normalizedChar < 0) normalizedChar += 26;

                // Convert back to ASCII and preserve case
                result.Append((char)(baseChar + normalizedChar));
            }
            else
            {
                // Non-alphabetic characters remain unchanged
                result.Append(inputChar);
            }
        }

        return result.ToString();
    }

    /// <summary>
    /// Decrypts the given text using the Caesar cipher
    /// </summary>
    /// <param name="text">The text to decrypt</param>
    /// <param name="key">The shift value (must be convertible to int)</param>
    /// <returns>The decrypted text</returns>
    public string Decrypt(string text, object key)
    {
        if (key is not int shift)
        {
            try
            {
                shift = Convert.ToInt32(key);
            }
            catch
            {
                throw new ArgumentException("Key must be convertible to an integer for Caesar cipher", nameof(key));
            }
        }

        // Decryption is just encryption with the negative shift
        return Encrypt(text, -shift);
    }
}
