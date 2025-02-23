class Program
{
    static async Task Main(string[] args)
    {
        var reader = new EmailReader(
            "imap_address", 
            993,                    
            "email",        
            "password"         
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