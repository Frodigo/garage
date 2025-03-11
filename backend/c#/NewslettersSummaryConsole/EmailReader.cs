using MailKit;
using MailKit.Net.Imap;
using MailKit.Search;
using MimeKit;

public class EmailReader
{
    private readonly ImapConnectionManager _connectionManager;
    private readonly ISummarizer _summarizer;
    
    public EmailReader(string host, int port, string username, string password)
    {
        _connectionManager = new ImapConnectionManager(host, port, username, password);
        _summarizer = new ClaudeSummarizer(Environment.GetEnvironmentVariable("CLAUDE_API_KEY") ?? throw new ArgumentNullException("CLAUDE_API_KEY is not set"));
    }
    
    public async Task ReadEmails(int maxEmails = 10)
    {
        using var client = await _connectionManager.ConnectAsync();
        var inbox = client.Inbox;
        await inbox.OpenAsync(FolderAccess.ReadOnly);
        
        Console.WriteLine($"Total emails: {inbox.Count}");
        var unreadCount = await inbox.SearchAsync(SearchQuery.NotSeen);
        Console.WriteLine($"Unread emails: {unreadCount.Count}");
        
        var uids = inbox.Search(SearchQuery.All).Reverse().Take(maxEmails);
        
        foreach (var uid in uids)
        {
            var message = inbox.GetMessage(uid);
            await ProcessEmail(message);
        }
        
        await client.DisconnectAsync(true);
    }
    
    private async Task ProcessEmail(MimeMessage message)
    {
        Console.WriteLine(EmailMessageFormatter.FormatEmailDetails(message));
        
        var content = message.TextBody ?? message.HtmlBody;
        
        if (!string.IsNullOrEmpty(content))
        {
            try
            {
                var summary = await _summarizer.SummarizeAsync(content, message.Subject);
                Console.WriteLine($"\nAI Summary:");
                Console.WriteLine(summary);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nFailed to generate summary: {ex.Message}");
            }
        }
        
        Console.WriteLine(EmailMessageFormatter.FormatAttachments(message));
    }

    public async Task ReadUnreadEmails(bool markAsRead = false)
    {
        using var client = await _connectionManager.ConnectAsync();
        var inbox = client.Inbox;
        await inbox.OpenAsync(markAsRead ? FolderAccess.ReadWrite : FolderAccess.ReadOnly);
        
        var query = SearchQuery.NotSeen;
        var uids = await inbox.SearchAsync(query);
        
        Console.WriteLine($"Found {uids.Count} unread messages");
        
        foreach (var uid in uids)
        {
            var message = await inbox.GetMessageAsync(uid);
            await ProcessEmail(message);
            
            if (markAsRead)
            {
                await inbox.AddFlagsAsync(uid, MessageFlags.Seen, true);
            }
        }
        
        await client.DisconnectAsync(true);
    }
}

