class Program
{
    static async Task Main(string[] args)
    {
        // Load environment variables
        DotNetEnv.Env.Load();
        
        var reader = new EmailReader(
            Environment.GetEnvironmentVariable("IMAP_ADDRESS") ?? throw new ArgumentNullException("IMAP_ADDRESS"),
            int.Parse(Environment.GetEnvironmentVariable("IMAP_PORT") ?? "993"),
            Environment.GetEnvironmentVariable("EMAIL") ?? throw new ArgumentNullException("EMAIL"),
            Environment.GetEnvironmentVariable("PASSWORD") ?? throw new ArgumentNullException("PASSWORD")
        );
        
        try
        {
            await reader.ReadEmails(1);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error occurred: {ex.Message}");
        }
    }
}