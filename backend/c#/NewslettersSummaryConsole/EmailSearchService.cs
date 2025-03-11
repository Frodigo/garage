using MailKit;
using MailKit.Net.Imap;
using MailKit.Search;
using MimeKit;

public class EmailSearchService
{
    private readonly ImapConnectionManager _connectionManager;
    private readonly EmailMessageFormatter _formatter;

    public EmailSearchService(ImapConnectionManager connectionManager)
    {
        _connectionManager = connectionManager;
        _formatter = new EmailMessageFormatter();
    }

    public async Task ReadAllEmails(int batchSize = 100)
    {
        using var client = await _connectionManager.ConnectAsync();
        var inbox = client.Inbox;
        await inbox.OpenAsync(FolderAccess.ReadOnly);
        
        var totalEmails = inbox.Count;
        Console.WriteLine($"Found {totalEmails} messages");
        
        for (int i = totalEmails; i > 0; i -= batchSize)
        {
            var start = Math.Max(i - batchSize, 0);
            var count = Math.Min(batchSize, i);
            
            var messages = await inbox.FetchAsync(start, count - 1, MessageSummaryItems.Full | MessageSummaryItems.UniqueId);
            
            foreach (var message in messages)
            {
                var fullMessage = await inbox.GetMessageAsync(message.UniqueId);
                Console.WriteLine(EmailMessageFormatter.FormatEmailDetails(fullMessage));
                Console.WriteLine($"Content: {fullMessage.TextBody ?? fullMessage.HtmlBody}");
                Console.WriteLine(EmailMessageFormatter.FormatAttachments(fullMessage));
            }
            
            Console.WriteLine($"Processed emails from {start + 1} to {start + count}");
        }
        
        await client.DisconnectAsync(true);
    }

    public async Task ReadEmailsBySubject(string searchSubject)
    {
        using var client = await _connectionManager.ConnectAsync();
        var inbox = client.Inbox;
        await inbox.OpenAsync(FolderAccess.ReadOnly);
        
        var query = SearchQuery.SubjectContains(searchSubject);
        var uids = inbox.Search(query);
        
        foreach (var uid in uids)
        {
            var message = inbox.GetMessage(uid);
            Console.WriteLine(EmailMessageFormatter.FormatEmailDetails(message));
        }
        
        await client.DisconnectAsync(true);
    }
} 