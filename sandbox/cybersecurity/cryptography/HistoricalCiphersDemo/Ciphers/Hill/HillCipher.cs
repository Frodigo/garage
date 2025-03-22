using System.Text;
using System.Numerics;

namespace HistoricalCiphersDemo.Ciphers.Hill;

/// <summary>
/// Implementation of the Hill cipher
/// </summary>
public class HillCipher : ICipher
{
    private const int AlphabetSize = 26;
    private const char BaseChar = 'A';
    private const char PaddingChar = 'X';

    /// <summary>
    /// Gets the name of the cipher
    /// </summary>
    public string Name => "Hill Cipher";
    
    /// <summary>
    /// Gets a description of how the cipher works
    /// </summary>
    public string Description => "The Hill cipher is a polygraphic substitution cipher based on linear algebra. " +
                                 "It encrypts blocks of letters using matrix multiplication.";
    
    /// <summary>
    /// Encrypts the given text using the Hill cipher
    /// </summary>
    /// <param name="text">The text to encrypt</param>
    /// <param name="key">The encryption key (must be a square matrix as int[,])</param>
    /// <returns>The encrypted text</returns>
    public string Encrypt(string text, object key)
    {
        if (string.IsNullOrEmpty(text))
            return string.Empty;
        
        // Validate and convert key
        int[,] matrix = ValidateAndConvertKey(key);
        int matrixSize = matrix.GetLength(0);
        
        // Process text
        string processedText = PrepareText(text, matrixSize);
        var result = new StringBuilder();
        
        // Process the text in blocks of size equal to the matrix dimension
        for (int i = 0; i < processedText.Length; i += matrixSize)
        {
            // Extract and process one block
            result.Append(ProcessBlock(processedText.Substring(i, matrixSize), matrix));
        }
        
        return result.ToString();
    }
    
    /// <summary>
    /// Decrypts the given text using the Hill cipher
    /// </summary>
    /// <param name="text">The text to decrypt</param>
    /// <param name="key">The decryption key (must be a square matrix as int[,])</param>
    /// <returns>The decrypted text</returns>
    public string Decrypt(string text, object key)
    {
        if (string.IsNullOrEmpty(text))
            return string.Empty;
        
        // Validate and convert key
        int[,] matrix = ValidateAndConvertKey(key);
        int matrixSize = matrix.GetLength(0);
        
        // Calculate inverse matrix for decryption
        int[,] inverseMatrix = CalculateInverseMatrix(matrix);
        
        // Process text
        string processedText = PrepareText(text, matrixSize);
        var result = new StringBuilder();
        
        // Process the text in blocks of size equal to the matrix dimension
        for (int i = 0; i < processedText.Length; i += matrixSize)
        {
            // Extract and process one block
            result.Append(ProcessBlock(processedText.Substring(i, matrixSize), inverseMatrix));
        }
        
        return result.ToString();
    }
    
    /// <summary>
    /// Processes a single block of text using the given matrix
    /// </summary>
    private string ProcessBlock(string block, int[,] matrix)
    {
        int size = matrix.GetLength(0);
        
        // Convert block to numeric values (A=0, B=1, etc.)
        int[] blockValues = new int[size];
        for (int i = 0; i < size; i++)
        {
            blockValues[i] = block[i] - BaseChar;
        }
        
        // Apply matrix transformation
        int[] resultValues = new int[size];
        for (int row = 0; row < size; row++)
        {
            resultValues[row] = 0;
            for (int col = 0; col < size; col++)
            {
                resultValues[row] = (resultValues[row] + matrix[row, col] * blockValues[col]);
            }
            resultValues[row] = ModuloPositive(resultValues[row], AlphabetSize);
        }
        
        // Convert back to characters
        var result = new StringBuilder(size);
        for (int i = 0; i < size; i++)
        {
            result.Append((char)(BaseChar + resultValues[i]));
        }
        
        return result.ToString();
    }
    
    /// <summary>
    /// Validates the key and converts it to the required matrix format
    /// </summary>
    private int[,] ValidateAndConvertKey(object key)
    {
        if (key is not int[,] matrix)
        {
            throw new ArgumentException("Key must be a square matrix (int[,]) for Hill cipher", nameof(key));
        }
        
        // Check if matrix is square
        if (matrix.GetLength(0) != matrix.GetLength(1))
        {
            throw new ArgumentException("Matrix must be square for Hill cipher", nameof(key));
        }
        
        return matrix;
    }
    
    /// <summary>
    /// Prepares the text for Hill cipher operations
    /// </summary>
    private string PrepareText(string text, int blockSize)
    {
        // Convert text to uppercase and remove non-alphabetic characters
        text = new string(text.ToUpper().Where(char.IsLetter).ToArray());
        
        // Pad the text if necessary to make its length a multiple of the block size
        if (text.Length % blockSize != 0)
        {
            text = text.PadRight(text.Length + (blockSize - text.Length % blockSize), PaddingChar);
        }
        
        return text;
    }
    
    /// <summary>
    /// Calculates the inverse of a matrix modulo 26
    /// </summary>
    private int[,] CalculateInverseMatrix(int[,] matrix)
    {
        int size = matrix.GetLength(0);
        
        // For 1x1 matrix, simply calculate the modular multiplicative inverse
        if (size == 1)
        {
            int value = matrix[0, 0];
            int inverse = FindModularMultiplicativeInverse(value, AlphabetSize);
            
            if (inverse == -1)
            {
                throw new ArgumentException($"The matrix value {value} is not invertible modulo {AlphabetSize}");
            }
            
            return new int[,] { { inverse } };
        }
        
        // For 2x2 matrix
        if (size == 2)
        {
            // Calculate determinant
            int det = (matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]);
            det = ModuloPositive(det, AlphabetSize);
            
            // Find modular multiplicative inverse of determinant
            int detInverse = FindModularMultiplicativeInverse(det, AlphabetSize);
            if (detInverse == -1)
            {
                throw new ArgumentException("The matrix is not invertible modulo 26. Choose a different key.");
            }
            
            // Calculate adjugate matrix
            int[,] adj = new int[2, 2];
            adj[0, 0] = matrix[1, 1];
            adj[0, 1] = -matrix[0, 1];
            adj[1, 0] = -matrix[1, 0];
            adj[1, 1] = matrix[0, 0];
            
            // Calculate inverse
            int[,] inverse = new int[2, 2];
            for (int i = 0; i < 2; i++)
            {
                for (int j = 0; j < 2; j++)
                {
                    inverse[i, j] = ModuloPositive(adj[i, j] * detInverse, AlphabetSize);
                }
            }
            
            return inverse;
        }
        
        // For 3x3 matrix
        if (size == 3)
        {
            // Calculate determinant using the formula:
            // |A| = a(ei-fh) - b(di-fg) + c(dh-eg)
            int a = matrix[0, 0], b = matrix[0, 1], c = matrix[0, 2];
            int d = matrix[1, 0], e = matrix[1, 1], f = matrix[1, 2];
            int g = matrix[2, 0], h = matrix[2, 1], i = matrix[2, 2];
            
            int det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
            det = ModuloPositive(det, AlphabetSize);
            
            // Find modular multiplicative inverse of determinant
            int detInverse = FindModularMultiplicativeInverse(det, AlphabetSize);
            if (detInverse == -1)
            {
                throw new ArgumentException("The 3x3 matrix is not invertible modulo 26. Choose a different key.");
            }
            
            // Calculate the cofactor matrix
            int[,] cofactor = new int[3, 3];
            
            cofactor[0, 0] = e * i - f * h;
            cofactor[0, 1] = -(d * i - f * g);
            cofactor[0, 2] = d * h - e * g;
            
            cofactor[1, 0] = -(b * i - c * h);
            cofactor[1, 1] = a * i - c * g;
            cofactor[1, 2] = -(a * h - b * g);
            
            cofactor[2, 0] = b * f - c * e;
            cofactor[2, 1] = -(a * f - c * d);
            cofactor[2, 2] = a * e - b * d;
            
            // Transpose the cofactor matrix to get the adjugate
            int[,] adj = new int[3, 3];
            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 3; col++)
                {
                    adj[row, col] = cofactor[col, row];
                }
            }
            
            // Calculate the inverse = adjugate * determinant^-1 mod 26
            int[,] inverse = new int[3, 3];
            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 3; col++)
                {
                    inverse[row, col] = ModuloPositive(adj[row, col] * detInverse, AlphabetSize);
                }
            }
            
            return inverse;
        }
        
        // For matrices larger than 3x3
        throw new NotImplementedException("Matrix inversion for sizes larger than 3x3 is not implemented.");
    }
    
    /// <summary>
    /// Calculates the positive modulo (handles negative numbers correctly)
    /// </summary>
    private int ModuloPositive(int value, int modulo)
    {
        return ((value % modulo) + modulo) % modulo;
    }
    
    /// <summary>
    /// Finds the modular multiplicative inverse using Extended Euclidean Algorithm
    /// </summary>
    /// <returns>The modular multiplicative inverse or -1 if it doesn't exist</returns>
    private int FindModularMultiplicativeInverse(int a, int m)
    {
        a = ModuloPositive(a, m);
        
        // Extended Euclidean Algorithm
        int m0 = m;
        int y = 0, x = 1;
 
        if (m == 1)
            return 0;
 
        while (a > 1)
        {
            // q is quotient
            int q = a / m;
            int t = m;
 
            // m is remainder now, process same as Euclid's algorithm
            m = a % m;
            a = t;
            t = y;
 
            // Update y and x
            y = x - q * y;
            x = t;
        }
 
        // Make x positive
        if (x < 0)
            x += m0;
 
        // Check if the inverse exists
        if (a != 1)
            return -1; // No modular multiplicative inverse exists
            
        return x;
    }
} 