using MimeKit;

namespace Core.Interfaces;

public interface IEmailProcessor
{
    Task ProcessEmailAsync(MimeMessage message);
    Task<string> GetEmailContentAsync(MimeMessage message);
} 