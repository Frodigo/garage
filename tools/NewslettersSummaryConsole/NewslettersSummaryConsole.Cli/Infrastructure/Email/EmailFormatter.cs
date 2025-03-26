using Core.Interfaces;
using MimeKit;

namespace Infrastructure.Email;

public class EmailFormatter : IEmailFormatter
{
    public string FormatEmailDetails(MimeMessage message)
    {
        return $"\n==========\nFrom: {message.From}\nTo: {message.To}\nSubject: {message.Subject}\nDate: {message.Date:g}\n==========\n";
    }

    public string FormatAttachments(MimeMessage message)
    {
        if (!message.Attachments.Any())
        {
            return "\nNo attachments\n==========\n";
        }

        var attachmentsList = string.Join("\n", message.Attachments.Select(a => $"- {a.ContentDisposition?.FileName ?? "Unnamed attachment"}"));
        return $"\nAttachments:\n{attachmentsList}\n==========\n";
    }

    public string FormatSummary(string summary)
    {
        return $"\nAI Summary:\n{summary}\n==========\n";
    }
} 