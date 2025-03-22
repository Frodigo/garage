using Xunit;
using HistoricalCiphersDemo.Ciphers.Caesar;

namespace HistoricalCiphersDemo.Tests;

[Collection("CipherTests")]
public class CaesarCipherTests
{
    [Fact]
    public void When_EncryptingLetterA_WithShiftOf1_ShouldReturnLetterB()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("A", 1);

        // Assert
        Assert.Equal("B", result);
    }

    [Fact]
    public void When_EncryptingLetterB_WithShiftOf1_ShouldReturnLetterC()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("B", 1);

        // Assert
        Assert.Equal("C", result);
    }

    [Fact]
    public void When_EncryptingLetterZ_WithShiftOf1_ShouldReturnLetterA()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("Z", 1);

        // Assert
        Assert.Equal("A", result);
    }

    [Fact]
    public void When_EncryptingLetterA_WithShiftOf3_ShouldReturnLetterD()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("A", 3);

        // Assert
        Assert.Equal("D", result);
    }

    [Fact]
    public void When_EncryptingLowercaseA_WithShiftOf1_ShouldReturnLowercaseB()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("a", 1);

        // Assert
        Assert.Equal("b", result);
    }

    [Fact]
    public void When_EncryptingABC_WithShiftOf1_ShouldReturnBCD()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("ABC", 1);

        // Assert
        Assert.Equal("BCD", result);
    }

    [Fact]
    public void When_EncryptingLetterA_WithShiftOf27_ShouldReturnLetterB()
    {
        var cipher = new CaesarCipher();
        var result = cipher.Encrypt("A", 27);
        Assert.Equal("B", result);
    }

    [Fact]
    public void When_EncryptingNonAlphabeticChars_ShouldLeaveThemUnchanged()
    {
        // Arrange
        var cipher = new CaesarCipher();

        // Act
        var result = cipher.Encrypt("A1 B2!", 1);

        // Assert
        Assert.Equal("B1 C2!", result);
    }

    [Fact]
    public void When_DecryptingEncryptedText_ShouldReturnOriginalText()
    {
        // Arrange
        var cipher = new CaesarCipher();
        var plainText = "Hello, World!";
        var shift = 5;
        var encryptedText = cipher.Encrypt(plainText, shift);

        // Act
        var decryptedText = cipher.Decrypt(encryptedText, shift);

        // Assert
        Assert.Equal(plainText, decryptedText);
    }

    [Fact]
    public void When_EncryptingLetterB_WithShiftOfMinus1_ShouldReturnLetterA()
    {
        var cipher = new CaesarCipher();
        var result = cipher.Encrypt("B", -1);
        Assert.Equal("A", result);
    }

    [Fact]
    public void When_EncryptingLetterA_WithShiftOfMinus1_ShouldReturnLetterZ()
    {
        var cipher = new CaesarCipher();
        var result = cipher.Encrypt("A", -1);
        Assert.Equal("Z", result);
    }

    [Fact]
    public void When_EncryptingEmptyString_ShouldReturnEmptyString()
    {
        var cipher = new CaesarCipher();
        var result = cipher.Encrypt("", 1);
        Assert.Equal("", result);
    }

    [Fact]
    public void When_EncryptingLongText_ShouldEncryptCorrectly()
    {
        var cipher = new CaesarCipher();
        var longText = "I love coding in C#";
        var expected = "J mpwf dpejoh jo D#";
        var result = cipher.Encrypt(longText, 1);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void When_EncryptingWithShiftOf0_ShouldReturnOriginalText()
    {
        var cipher = new CaesarCipher();
        var text = "HELLO";
        var result = cipher.Encrypt(text, 0);
        Assert.Equal(text, result);
    }

    [Fact]
    public void When_EncryptingWithShiftOf26_ShouldReturnOriginalText()
    {
        var cipher = new CaesarCipher();
        var text = "HELLO";
        var result = cipher.Encrypt(text, 26);
        Assert.Equal(text, result);
    }
} 