using Core.Interfaces;
using MailKit;
using MailKit.Search;

namespace Core.Services;

public class EmailService
{
    private readonly IEmailConnectionManager _connectionManager;
    private readonly IEmailProcessor _emailProcessor;

    public EmailService(IEmailConnectionManager connectionManager, IEmailProcessor emailProcessor)
    {
        _connectionManager = connectionManager;
        _emailProcessor = emailProcessor;
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
            await _emailProcessor.ProcessEmailAsync(message);
        }
        
        await _connectionManager.DisconnectAsync(client);
    }

    public async Task ReadUnreadEmails(int maxEmails = 10, bool markAsRead = false)
    {
        using var client = await _connectionManager.ConnectAsync();
        var inbox = client.Inbox;
        await inbox.OpenAsync(markAsRead ? FolderAccess.ReadWrite : FolderAccess.ReadOnly);
        
        var query = SearchQuery.NotSeen;
        var uids = await inbox.SearchAsync(query);
        
        Console.WriteLine($"Found {uids.Count} unread messages");
        
        foreach (var uid in uids.Take(maxEmails))
        {
            var message = await inbox.GetMessageAsync(uid);
            await _emailProcessor.ProcessEmailAsync(message);
            
            if (markAsRead)
            {
                await inbox.AddFlagsAsync(uid, MessageFlags.Seen, true);
            }
        }
        
        await _connectionManager.DisconnectAsync(client);
    }
} 