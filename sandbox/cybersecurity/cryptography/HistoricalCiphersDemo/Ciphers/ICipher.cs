namespace HistoricalCiphersDemo.Ciphers;

public interface ICipher
{
    string Encrypt(string text, object key);
    string Decrypt(string text, object key);
    string Name { get; }
    string Description { get; }
}