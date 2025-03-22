namespace HistoricalCiphersDemo.Ciphers.Vigenère;

public class VigenèreCipher: ICipher
{
    public string Name => "Vigenère";
    
    public string Description => "A polyalphabetic substitution cipher that uses a keyword to determine shifting.";

    public string Encrypt(string text, object key)
    {
        return ProcessText(text, key.ToString()!, true);
    }   

    public string Decrypt(string text, object key)
    {
        return ProcessText(text, key.ToString()!, false);
    }
    
    private string ProcessText(string text, string key, bool encrypt)
    {
        if (string.IsNullOrEmpty(text) || string.IsNullOrEmpty(key))
            return string.Empty;
            
        char[] result = new char[text.Length];
        int keyIndex = 0;
        
        for (int i = 0; i < text.Length; i++)
        {
            char textChar = text[i];
            
            // Skip non-alphabetic characters
            if (!char.IsLetter(textChar))
            {
                result[i] = textChar;
                continue;
            }
            
            // Get the corresponding key character (cycling through the key)
            // Only advance key index for alphabetic characters
            char keyChar = key[keyIndex % key.Length];
            keyIndex++;
            
            // Calculate the shift based on the key character
            int shift = char.ToUpper(keyChar) - 'A';
            
            // Handle encryption vs decryption
            if (!encrypt)
                shift = -shift;
                
            // Determine base value ('A' for uppercase, 'a' for lowercase)
            char baseChar = char.IsUpper(textChar) ? 'A' : 'a';
            
            // Apply the shift, ensuring positive modulo
            result[i] = (char)(((textChar - baseChar + shift + 26) % 26) + baseChar);
        }
        
        return new string(result);
    }
}