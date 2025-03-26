using MimeKit;

namespace Core.Interfaces;

public interface IEmailFormatter
{
    string FormatEmailDetails(MimeMessage message);
    string FormatAttachments(MimeMessage message);
    string FormatSummary(string summary);
} 