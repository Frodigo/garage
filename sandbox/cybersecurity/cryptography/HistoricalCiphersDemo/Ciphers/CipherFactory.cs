namespace HistoricalCiphersDemo.Ciphers;

/// <summary>
/// Factory for creating and retrieving cipher implementations
/// </summary>
public class CipherFactory
{
    private readonly Dictionary<string, ICipher> _ciphers = new Dictionary<string, ICipher>(StringComparer.OrdinalIgnoreCase);
    
    /// <summary>
    /// Registers a cipher implementation
    /// </summary>
    /// <param name="cipher">The cipher implementation to register</param>
    public void RegisterCipher(ICipher cipher)
    {
        if (cipher == null)
            throw new ArgumentNullException(nameof(cipher));
            
        _ciphers[cipher.Name] = cipher;
    }
    
    /// <summary>
    /// Gets a cipher implementation by name
    /// </summary>
    /// <param name="name">The name of the cipher</param>
    /// <returns>The cipher implementation</returns>
    public ICipher GetCipher(string name)
    {
        if (string.IsNullOrEmpty(name))
            throw new ArgumentException("Cipher name cannot be null or empty", nameof(name));
            
        if (!_ciphers.TryGetValue(name, out var cipher))
            throw new ArgumentException($"No cipher registered with name '{name}'", nameof(name));
            
        return cipher;
    }
    
    /// <summary>
    /// Gets all registered ciphers
    /// </summary>
    /// <returns>A collection of registered ciphers</returns>
    public IEnumerable<ICipher> GetAllCiphers()
    {
        return _ciphers.Values;
    }
} 