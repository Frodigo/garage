using Xunit;
using HistoricalCiphersDemo.Ciphers.Vigenère;

namespace HistoricalCiphersDemo.Tests;

[Collection("CipherTests")]
public class VigenèreCipherTests
{
    [Fact]
    public void When_EncryptingLetterA_WithKeyOfB_ShouldReturnLetterB()
    {
        // Arrange
        string plaintext = "A";
        string key = "B";
        string expected = "B";

        var cipher = new VigenèreCipher();

        // Act
        string actual = cipher.Encrypt(plaintext, key);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void When_EncryptingLetterB_WithKeyOfC_ShouldReturnLetterD()
    {
        // Arrange
        string plaintext = "B";
        string key = "C";
        string expected = "D";

        var cipher = new VigenèreCipher();

        // Act
        string actual = cipher.Encrypt(plaintext, key);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void When_EncryptingWord_WithMultiCharKey_ShouldEncryptCorrectly()
    {
        // Arrange
        string plaintext = "HELLO";
        string key = "KEY";
        string expected = "RIJVS";

        var cipher = new VigenèreCipher();

        // Act
        string actual = cipher.Encrypt(plaintext, key);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void When_EncryptingMixedCaseWithSpecialChars_ShouldPreserveCaseAndSpecialChars()
    {
        // Arrange
        string plaintext = "Hello, World!";
        string key = "KEY";
        string expected = "Rijvs, Uyvjn!";

        var cipher = new VigenèreCipher();

        // Act
        string actual = cipher.Encrypt(plaintext, key);

        // Assert
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void When_DecryptingMixedCaseWithSpecialChars_WithKey_ShouldReturnOriginalPlaintext()
    {
        // Arrange
        string ciphertext = "Rijvs, Uyvjn!";
        string key = "KEY";
        string expected = "Hello, World!";

        var cipher = new VigenèreCipher();

        // Act
        string actual = cipher.Decrypt(ciphertext, key);

        // Assert
        Assert.Equal(expected, actual);
    }
}
