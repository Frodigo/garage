using HistoricalCiphersDemo.Ciphers;
using HistoricalCiphersDemo.Ciphers.Caesar;
using HistoricalCiphersDemo.Ciphers.Vigenère;
using HistoricalCiphersDemo.Ciphers.Hill;

namespace HistoricalCiphersDemo;

public class Program
{
    private static CipherFactory _cipherFactory = new CipherFactory();

    public static void Main(string[] args)
    {
        Console.WriteLine("=== Historical Ciphers Demo ===");
        Console.WriteLine();

        // Register ciphers
        _cipherFactory.RegisterCipher(new CaesarCipher());
        _cipherFactory.RegisterCipher(new VigenèreCipher());
        _cipherFactory.RegisterCipher(new HillCipher());
        // Main menu
        RunMainMenu();
    }

    private static void RunMainMenu()
    {
        while (true)
        {
            Console.Clear();
            Console.WriteLine("=== Historical Ciphers Demo ===");
            Console.WriteLine();
            Console.WriteLine("Available ciphers:");

            var ciphers = _cipherFactory.GetAllCiphers().ToList();
            for (int i = 0; i < ciphers.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {ciphers[i].Name}");
            }

            Console.WriteLine();
            Console.WriteLine("0. Exit");
            Console.WriteLine();
            Console.Write("Select a cipher (number): ");

            string? input = Console.ReadLine();

            if (input == "0")
                return;

            if (int.TryParse(input, out int selection) && selection > 0 && selection <= ciphers.Count)
            {
                var selectedCipher = ciphers[selection - 1];
                RunCipherMenu(selectedCipher);
            }
            else
            {
                Console.WriteLine("Invalid selection. Press any key to continue...");
                Console.ReadKey(true);
            }
        }
    }

    private static void RunCipherMenu(ICipher cipher)
    {
        while (true)
        {
            Console.Clear();
            Console.WriteLine($"=== {cipher.Name} ===");
            Console.WriteLine();
            Console.WriteLine(cipher.Description);
            Console.WriteLine();
            Console.WriteLine("1. Encrypt a message");
            Console.WriteLine("2. Decrypt a message");
            Console.WriteLine("0. Back to main menu");
            Console.WriteLine();
            Console.Write("Select an option: ");

            string? input = Console.ReadLine();

            if (input == "0")
                return;

            if (input == "1")
            {
                EncryptMessage(cipher);
            }
            else if (input == "2")
            {
                DecryptMessage(cipher);
            }
            else
            {
                Console.WriteLine("Invalid selection. Press any key to continue...");
                Console.ReadKey(true);
            }
        }
    }

    private static void EncryptMessage(ICipher cipher)
    {
        Console.Clear();
        Console.WriteLine($"=== {cipher.Name} - Encryption ===");
        Console.WriteLine();

        Console.WriteLine("Enter a message to encrypt:");
        string? message = Console.ReadLine();

        if (string.IsNullOrEmpty(message))
        {
            Console.WriteLine("Message cannot be empty. Press any key to continue...");
            Console.ReadKey(true);
            return;
        }

        object key = GetCipherKey(cipher);

        try
        {
            string encrypted = cipher.Encrypt(message, key);

            Console.WriteLine();
            Console.WriteLine("Encrypted message:");
            Console.WriteLine(encrypted);
            Console.WriteLine();
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey(true);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey(true);
        }
    }

    private static void DecryptMessage(ICipher cipher)
    {
        Console.Clear();
        Console.WriteLine($"=== {cipher.Name} - Decryption ===");
        Console.WriteLine();

        Console.WriteLine("Enter a message to decrypt:");
        string? message = Console.ReadLine();

        if (string.IsNullOrEmpty(message))
        {
            Console.WriteLine("Message cannot be empty. Press any key to continue...");
            Console.ReadKey(true);
            return;
        }

        object key = GetCipherKey(cipher);

        try
        {
            string decrypted = cipher.Decrypt(message, key);

            Console.WriteLine();
            Console.WriteLine("Decrypted message:");
            Console.WriteLine(decrypted);
            Console.WriteLine();
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey(true);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            Console.WriteLine("Press any key to continue...");
            Console.ReadKey(true);
        }
    }

    private static object GetCipherKey(ICipher cipher)
    {
        if (cipher is CaesarCipher)
        {
            Console.WriteLine("Enter the shift value (positive or negative integer):");
            if (!int.TryParse(Console.ReadLine(), out int shift))
            {
                throw new ArgumentException("Invalid shift value. Must be an integer.");
            }

            return shift;
        }

        if (cipher is HillCipher)
        {
            Console.WriteLine("Enter the matrix size (1, 2, or 3):");
            if (!int.TryParse(Console.ReadLine(), out int size) || size < 1 || size > 3)
            {
                throw new ArgumentException("Matrix size must be 1, 2, or 3.");
            }

            int[,] matrix = new int[size, size];

            Console.WriteLine($"Enter the {size}x{size} matrix values (one row per line, space-separated):");
            Console.WriteLine("Example for 2x2 matrix:");
            Console.WriteLine("3 2");
            Console.WriteLine("5 7");

            for (int i = 0; i < size; i++)
            {
                Console.Write($"Row {i + 1}: ");
                string? line = Console.ReadLine();
                if (string.IsNullOrEmpty(line))
                {
                    throw new ArgumentException($"Row {i + 1} cannot be empty.");
                }

                string[] values = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (values.Length != size)
                {
                    throw new ArgumentException($"Expected {size} values for row {i + 1}, got {values.Length}.");
                }

                for (int j = 0; j < size; j++)
                {
                    if (!int.TryParse(values[j], out int value))
                    {
                        throw new ArgumentException($"Invalid number at position [{i},{j}]: {values[j]}");
                    }
                    matrix[i, j] = value;
                }
            }

            return matrix;
        }

        // Default key input for other ciphers
        Console.WriteLine("Enter the key:");
        string? key = Console.ReadLine();

        if (string.IsNullOrEmpty(key))
        {
            throw new ArgumentException("Key cannot be empty.");
        }

        return key;
    }
}
