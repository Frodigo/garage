using CesarCipherLib;
using System;

namespace CesarCipherDemo;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("=== Caesar Cipher Demo ===");
        Console.WriteLine();

        var cipher = new CesarCipher();
        
        // Example 1 - Basic encryption and decryption
        string message1 = "HELLO WORLD";
        int shift1 = 3;
        string encrypted1 = cipher.Encrypt(message1, shift1);
        
        Console.WriteLine("Example 1 - Basic Encryption:");
        Console.WriteLine($"Original: {message1}");
        Console.WriteLine($"Shift: {shift1}");
        Console.WriteLine($"Encrypted: {encrypted1}");
        Console.WriteLine($"Decrypted: {cipher.Decrypt(encrypted1, shift1)}");
        Console.WriteLine();
        
        // Example 2 - Mixed case and special characters
        string message2 = "Hello, World! 123";
        int shift2 = 7;
        string encrypted2 = cipher.Encrypt(message2, shift2);
        
        Console.WriteLine("Example 2 - Mixed Case and Special Characters:");
        Console.WriteLine($"Original: {message2}");
        Console.WriteLine($"Shift: {shift2}");
        Console.WriteLine($"Encrypted: {encrypted2}");
        Console.WriteLine($"Decrypted: {cipher.Decrypt(encrypted2, shift2)}");
        Console.WriteLine();
        
        // Example 3 - Negative shift
        string message3 = "NEGATIVE SHIFT EXAMPLE";
        int shift3 = -5;
        string encrypted3 = cipher.Encrypt(message3, shift3);
        
        Console.WriteLine("Example 3 - Negative Shift:");
        Console.WriteLine($"Original: {message3}");
        Console.WriteLine($"Shift: {shift3}");
        Console.WriteLine($"Encrypted: {encrypted3}");
        Console.WriteLine($"Decrypted: {cipher.Decrypt(encrypted3, shift3)}");
        Console.WriteLine();
        
        // Interactive mode
        Console.WriteLine("=== Interactive Mode ===");
        RunInteractiveMode(cipher);
    }
    
    private static void RunInteractiveMode(CesarCipher cipher)
    {
        Console.WriteLine("Enter a message to encrypt (or press Enter to exit):");
        string? message = Console.ReadLine();
        
        if (string.IsNullOrEmpty(message))
            return;
            
        Console.WriteLine("Enter the shift value (positive or negative integer):");
        if (!int.TryParse(Console.ReadLine(), out int shift))
        {
            Console.WriteLine("Invalid shift value. Using default shift of 3.");
            shift = 3;
        }
        
        string encrypted = cipher.Encrypt(message, shift);
        Console.WriteLine($"Encrypted: {encrypted}");
        Console.WriteLine($"Decrypted: {cipher.Decrypt(encrypted, shift)}");
        
        Console.WriteLine();
        RunInteractiveMode(cipher); // Allow multiple encryptions
    }
}
