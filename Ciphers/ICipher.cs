namespace HistoricalCiphersDemo.Ciphers;

/// <summary>
/// Interface for cipher implementations
/// </summary>
public interface ICipher
{
    /// <summary>
    /// Encrypts the given text using the cipher algorithm
    /// </summary>
    /// <param name="text">The text to encrypt</param>
    /// <param name="key">The encryption key (interpretation depends on the specific cipher)</param>
    /// <returns>The encrypted text</returns>
    string Encrypt(string text, object key);
    
    /// <summary>
    /// Decrypts the given text using the cipher algorithm
    /// </summary>
    /// <param name="text">The text to decrypt</param>
    /// <param name="key">The decryption key (interpretation depends on the specific cipher)</param>
    /// <returns>The decrypted text</returns>
    string Decrypt(string text, object key);
    
    /// <summary>
    /// Gets the name of the cipher
    /// </summary>
    string Name { get; }
    
    /// <summary>
    /// Gets a description of how the cipher works
    /// </summary>
    string Description { get; }
} 