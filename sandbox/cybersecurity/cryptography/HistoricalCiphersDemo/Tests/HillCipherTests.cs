using Xunit;
using HistoricalCiphersDemo.Ciphers.Hill;

namespace HistoricalCiphersDemo.Tests;

[Collection("CipherTests")]
public class HillCipherTests
{
    [Fact]
    public void When_EncryptingA_WithIdentityMatrix_ShouldReturnA()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { { 1 } };

        // Act
        var result = cipher.Encrypt("A", key);

        // Assert
        Assert.Equal("A", result);
    }

    [Fact]
    public void When_EncryptingAB_With2x2Matrix_ShouldEncryptCorrectly()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 2, 3 }, 
            { 1, 4 } 
        };

        // Act
        var result = cipher.Encrypt("AB", key);

        // Assert
        Assert.Equal("DE", result);
    }
    
    [Fact]
    public void When_EncryptingHELP_With2x2Matrix_ShouldEncryptCorrectly()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 3, 2 }, 
            { 5, 7 } 
        };

        // Act
        var result = cipher.Encrypt("HELP", key);

        // Assert
        Assert.Equal("DLLE", result);
    }
    
    [Fact]
    public void When_DecryptingCF_With2x2Matrix_ShouldReturnAB()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 2, 3 }, 
            { 1, 4 } 
        };
        
        // Act
        var result = cipher.Decrypt("DE", key);
        
        // Assert
        Assert.Equal("AB", result);
    }
    
    [Fact]
    public void When_DecryptingDLLE_With2x2Matrix_ShouldReturnHELP()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 3, 2 }, 
            { 5, 7 } 
        };
        
        // Act
        var result = cipher.Decrypt("DLLE", key);
        
        // Assert
        Assert.Equal("HELP", result);
    }
    
    [Fact]
    public void When_EncryptingTextAndThenDecrypting_ShouldReturnOriginalText()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 5, 8 }, 
            { 17, 3 } 
        };
        var plainText = "CRYPTO";
        
        // Act
        var encryptedText = cipher.Encrypt(plainText, key);
        var decryptedText = cipher.Decrypt(encryptedText, key);
        
        // Assert
        Assert.Equal(plainText, decryptedText);
    }
    
    [Fact]
    public void When_Using3x3Matrix_ShouldEncryptAndDecryptCorrectly()
    {
        // Arrange
        var cipher = new HillCipher();
        var key = new int[,] { 
            { 6, 24, 1 }, 
            { 13, 16, 10 }, 
            { 20, 17, 15 } 
        };
        var plainText = "THEMATRIXHAS";
        
        // Act
        var encryptedText = cipher.Encrypt(plainText, key);
        var decryptedText = cipher.Decrypt(encryptedText, key);
        
        // Assert
        Assert.Equal(plainText, decryptedText);
    }
} 