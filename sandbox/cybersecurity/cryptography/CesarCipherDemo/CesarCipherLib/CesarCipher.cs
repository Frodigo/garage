namespace CesarCipherLib;

public class CesarCipher
{
    public string Encrypt(string text, int shift)
    {
        if (string.IsNullOrEmpty(text))
            return string.Empty;

        var result = new System.Text.StringBuilder();
        
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
    
    public string Decrypt(string text, int shift)
    {
        // Decryption is just encryption with the negative shift
        return Encrypt(text, -shift);
    }
} 