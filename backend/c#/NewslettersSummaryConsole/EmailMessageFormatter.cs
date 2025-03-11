using MimeKit;

public class EmailMessageFormatter
{
    public static string FormatEmailDetails(MimeMessage message)
    {
        return $"""
            ------------------------
            From: {message.From}
            To: {message.To}
            Subject: {message.Subject}
            Date: {message.Date.ToLocalTime():g}
            """;
    }

    public static string FormatAttachments(MimeMessage message)
    {
        if (!message.Attachments.Any())
            return string.Empty;

        var result = "\nAttachments:\n";
        foreach (var attachment in message.Attachments)
        {
            if (attachment is MessagePart rfc822)
            {
                result += $"- Attached email: {rfc822.Message.Subject}\n";
            }
            else
            {
                var fileName = attachment.ContentDisposition?.FileName ?? attachment.ContentType.Name;
                result += $"- {fileName}\n";
            }
        }
        return result;
    }
} 