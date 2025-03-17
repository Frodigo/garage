using Core.Interfaces;
using Core.Models;
using System.Text.RegularExpressions;

namespace Infrastructure.Files;

public class SummaryFileService : ISummaryFileService
{
    private readonly string _summariesPath;

    public SummaryFileService(string summariesPath)
    {
        _summariesPath = summariesPath;
        if (!Directory.Exists(_summariesPath))
        {
            Directory.CreateDirectory(_summariesPath);
        }
    }

    public async Task SaveSummaryAsync(string subject, string summary, string originalContent, string sender, EmailMetadata metadata)
    {
        var filePath = GetSummaryPath(subject, sender);
        var directoryPath = Path.GetDirectoryName(filePath);
        
        if (directoryPath != null && !Directory.Exists(directoryPath))
        {
            Directory.CreateDirectory(directoryPath);
        }

        var content = FormatContentWithMetadata(summary, originalContent, metadata);
        await File.WriteAllTextAsync(filePath, content);
    }

    public string GetSummaryPath(string subject, string sender)
    {
        var sanitizedSender = SanitizeFileName(sender);
        var sanitizedSubject = SanitizeFileName(subject);
        return Path.Combine(_summariesPath, sanitizedSender, $"{DateTime.Now:yyyy-MM-dd}_{sanitizedSubject}.md");
    }

    private static string FormatContentWithMetadata(string summary, string originalContent, EmailMetadata metadata)
    {
        var yaml = $"""
        ---
        subject: "{metadata.Subject}"
        sender: "{metadata.Sender}"
        sender_name: "{metadata.SenderName}"
        date: {metadata.Date:yyyy-MM-dd HH:mm:ss}
        summarizer: {metadata.Summarizer}
        recipients: "{metadata.Recipients}"
        has_attachments: {metadata.HasAttachments.ToString().ToLower()}
        ---

        ## AI Summary
        {summary}

        ## Original Content
        {originalContent}
        """;

        return yaml;
    }

    private static string SanitizeFileName(string fileName)
    {
        // Remove invalid characters from the filename
        var invalidChars = Regex.Escape(new string(Path.GetInvalidFileNameChars()));
        var invalidRegEx = string.Format(@"([{0}]*\.+$)|([{0}]+)", invalidChars);
        
        return Regex.Replace(fileName, invalidRegEx, "_");
    }
} 