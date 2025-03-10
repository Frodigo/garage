using MailKit;
using MailKit.Net.Imap;
using MailKit.Search;
using MimeKit;

public class EmailReader
{
    private readonly string _host;
    private readonly int _port;
    private readonly string _username;
    private readonly string _password;
    //private readonly OllamaSummarizer _summarizer;

    private readonly ClaudeSummarizer _summarizer;
    
    public EmailReader(string host, int port, string username, string password)
    {
        _host = host;
        _port = port;
        _username = username;
        _password = password;
        _summarizer = new ClaudeSummarizer(Environment.GetEnvironmentVariable("CLAUDE_API_KEY") ?? throw new ArgumentNullException("CLAUDE_API_KEY is not set"));
    }
    
    public async Task ReadEmails(int maxEmails = 10)
    {
        using (var client = new ImapClient())
        {
            // Connect to the server
            await client.ConnectAsync(_host, _port, true);
            
            // Login
            await client.AuthenticateAsync(_username, _password);
            
            // Select the inbox
            var inbox = client.Inbox;
            await inbox.OpenAsync(FolderAccess.ReadOnly);
            
            Console.WriteLine($"Total emails: {inbox.Count}");
            var unreadCount = await inbox.SearchAsync(SearchQuery.NotSeen);
            Console.WriteLine($"Unread emails: {unreadCount.Count}");
            
            // Get the last n emails
            var uids = inbox.Search(SearchQuery.All).Reverse().Take(maxEmails);
            
            foreach (var uid in uids)
            {
                var message = inbox.GetMessage(uid);
                await SummarizeEmail(message);
            }
            
            await client.DisconnectAsync(true);
        }
    }
    
    private async Task SummarizeEmail(MimeMessage message)
    {
        Console.WriteLine("\n------------------------");
        Console.WriteLine($"From: {message.From}");
        Console.WriteLine($"To: {message.To}");
        Console.WriteLine($"Subject: {message.Subject}");
        Console.WriteLine($"Date: {message.Date.ToLocalTime():g}");
        
        var content = message.TextBody ?? message.HtmlBody;
        
        if (!string.IsNullOrEmpty(content))
        {
            try
            {
                var summary = await _summarizer.SummarizeAsync(content);
                Console.WriteLine($"\nAI Summary:");
                Console.WriteLine(summary);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nFailed to generate summary: {ex.Message}");
            }
        }
        
        if (message.Attachments.Any())
        {
            Console.WriteLine("\nAttachments:");
            foreach (var attachment in message.Attachments)
            {
                if (attachment is MessagePart rfc822)
                {
                    Console.WriteLine($"- Attached email: {rfc822.Message.Subject}");
                }
                else
                {
                    var fileName = attachment.ContentDisposition?.FileName ?? attachment.ContentType.Name;
                    Console.WriteLine($"- {fileName}");
                }
            }
        }
    }

    public async Task ReadUnreadEmails(bool markAsRead = false)
    {
        using (var client = new ImapClient())
        {
            await client.ConnectAsync(_host, _port, true);
            await client.AuthenticateAsync(_username, _password);
            
            var inbox = client.Inbox;
            await inbox.OpenAsync(markAsRead ? FolderAccess.ReadWrite : FolderAccess.ReadOnly);
            
            var query = SearchQuery.NotSeen;
            var uids = await inbox.SearchAsync(query);
            
            Console.WriteLine($"Found {uids.Count} unread messages");
            
            foreach (var uid in uids)
            {
                var message = await inbox.GetMessageAsync(uid);
                await SummarizeEmail(message);
                
                if (markAsRead)
                {
                    await inbox.AddFlagsAsync(uid, MessageFlags.Seen, true);
                }
            }
            
            await client.DisconnectAsync(true);
        }
    }

    public async Task ReadAllEmails(int batchSize = 100)
    {
        using (var client = new ImapClient())
        {
            await client.ConnectAsync(_host, _port, true);
            await client.AuthenticateAsync(_username, _password);
            
            var inbox = client.Inbox;
            await inbox.OpenAsync(FolderAccess.ReadOnly);
            
            var totalEmails = inbox.Count;
            Console.WriteLine($"Found {totalEmails} messages");
            
            // processing emails in batches
            for (int i = totalEmails; i > 0; i -= batchSize)
            {
                var start = Math.Max(i - batchSize, 0);
                var count = Math.Min(batchSize, i);
                
                var messages = await inbox.FetchAsync(start, count - 1, MessageSummaryItems.Full | MessageSummaryItems.UniqueId);
                
                foreach (var message in messages)
                {
                    var fullMessage = await inbox.GetMessageAsync(message.UniqueId);
                    Console.WriteLine($"------------------------");
                    Console.WriteLine($"Od: {fullMessage.From}");
                    Console.WriteLine($"Do: {fullMessage.To}");
                    Console.WriteLine($"Temat: {fullMessage.Subject}");
                    Console.WriteLine($"Data: {fullMessage.Date}");
                    Console.WriteLine($"Treść: {fullMessage.TextBody ?? fullMessage.HtmlBody}");
                    
                    // saving attachments
                    foreach (var attachment in fullMessage.Attachments)
                    {
                        if (attachment is MessagePart rfc822)
                        {
                            Console.WriteLine($"Załączony mail: {rfc822.Message.Subject}");
                        }
                        else
                        {
                            var fileName = attachment.ContentDisposition?.FileName ?? attachment.ContentType.Name;
                            Console.WriteLine($"Załącznik: {fileName}");
                        }
                    }
                }
                
                Console.WriteLine($"Przetworzono maile od {start + 1} do {start + count}");
            }
            
            await client.DisconnectAsync(true);
        }
    }

    public async Task ReadEmailsBySubject(string searchSubject)
    {
        using (var client = new ImapClient())
        {
            await client.ConnectAsync(_host, _port, true);
            await client.AuthenticateAsync(_username, _password);
            
            var inbox = client.Inbox;
            await inbox.OpenAsync(FolderAccess.ReadOnly);
            
            var query = SearchQuery.SubjectContains(searchSubject);
            var uids = inbox.Search(query);
            
            foreach (var uid in uids)
            {
                var message = inbox.GetMessage(uid);
                Console.WriteLine($"------------------------");
                Console.WriteLine($"Od: {message.From}");
                Console.WriteLine($"Temat: {message.Subject}");
                Console.WriteLine($"Data: {message.Date}");
            }
            
            await client.DisconnectAsync(true);
        }
    }
}

