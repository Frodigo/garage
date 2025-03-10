class Program
{
    static async Task Main(string[] args)
    {
        // Wczytaj zmienne środowiskowe z pliku .env
        DotNetEnv.Env.Load();
        
        var reader = new EmailReader(
            Environment.GetEnvironmentVariable("IMAP_ADDRESS") ?? throw new ArgumentNullException("IMAP_ADDRESS"),
            int.Parse(Environment.GetEnvironmentVariable("IMAP_PORT") ?? "993"),
            Environment.GetEnvironmentVariable("EMAIL") ?? throw new ArgumentNullException("EMAIL"),
            Environment.GetEnvironmentVariable("PASSWORD") ?? throw new ArgumentNullException("PASSWORD")
        );
        
        try
        {
            // Read last 5 emails
            //await reader.ReadEmails(10);

            await reader.ReadUnreadEmails();
            
            // // read all emails (in batches of 100)
            // await reader.ReadAllEmails(100);
            
            // // search emails by subject
            // await reader.ReadEmailsBySubject("ważne");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error occurred: {ex.Message}");
        }
    }
}