using Core.Interfaces;
using MailKit;
using MailKit.Net.Imap;
using MailKit.Security;

namespace Infrastructure.Email;

public class ImapConnectionManager : IEmailConnectionManager
{
    private readonly string _host;
    private readonly int _port;
    private readonly string _username;
    private readonly string _password;

    public ImapConnectionManager(string host, int port, string username, string password)
    {
        _host = host;
        _port = port;
        _username = username;
        _password = password;
    }

    public async Task<IImapClient> ConnectAsync()
    {
        var client = new ImapClient();
        await client.ConnectAsync(_host, _port, SecureSocketOptions.SslOnConnect);
        await client.AuthenticateAsync(_username, _password);
        return client;
    }

    public async Task DisconnectAsync(IImapClient client, bool quit = true)
    {
        if (client != null)
        {
            await client.DisconnectAsync(quit);
        }
    }
} 