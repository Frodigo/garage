using MailKit.Net.Imap;

namespace Core.Interfaces;

public interface IEmailConnectionManager
{
    Task<IImapClient> ConnectAsync();
    Task DisconnectAsync(IImapClient client, bool quit = true);
} 