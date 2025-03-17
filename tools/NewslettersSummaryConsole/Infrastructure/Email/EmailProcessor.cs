using Core.Interfaces;
using Core.Models;
using MimeKit;
using NewslettersSummaryConsole.Core;

namespace Infrastructure.Email;

public class EmailProcessor : IEmailProcessor
{
    private readonly ISummarizer _summarizer;
    private readonly IEmailFormatter _formatter;
    private readonly ISummaryFileService _summaryFileService;
    private readonly string _activeSummarizer;
    private readonly List<ProcessedEmailInfo> _processedEmails;

    public EmailProcessor(ISummarizer summarizer, IEmailFormatter formatter, ISummaryFileService summaryFileService, string activeSummarizer)
    {
        _summarizer = summarizer;
        _formatter = formatter;
        _summaryFileService = summaryFileService;
        _activeSummarizer = activeSummarizer;
        _processedEmails = new List<ProcessedEmailInfo>();
    }

    public async Task ProcessEmailAsync(MimeMessage message)
    {
        Console.WriteLine(_formatter.FormatEmailDetails(message));
        
        var content = await GetEmailContentAsync(message);
        if (!string.IsNullOrEmpty(content))
        {
            try
            {
                var summary = await _summarizer.SummarizeAsync(content, message.Subject);
                Console.WriteLine(_formatter.FormatSummary(summary));
                
                // Get sender's email address and create metadata
                var sender = message.From.First();
                var metadata = new EmailMetadata
                {
                    Subject = message.Subject ?? "No Subject",
                    Sender = sender.ToString(),
                    SenderName = (sender as MailboxAddress)?.Name ?? "Unknown",
                    Date = message.Date.DateTime,
                    Summarizer = _activeSummarizer,
                    Recipients = string.Join(", ", message.To.Select(r => r.ToString())),
                    HasAttachments = message.Attachments.Any()
                };
                
                // Save summary to file
                var filePath = _summaryFileService.GetSummaryPath(message.Subject!, metadata.Sender);
                await _summaryFileService.SaveSummaryAsync(message.Subject!, summary, content, metadata.Sender, metadata);
                Console.WriteLine($"Summary saved to: {filePath}");

                // Add to processed emails list
                _processedEmails.Add(new ProcessedEmailInfo
                {
                    Subject = message.Subject ?? "No Subject",
                    Sender = metadata.Sender,
                    SenderName = metadata.SenderName,
                    Date = metadata.Date,
                    FilePath = filePath,
                    HasAttachments = metadata.HasAttachments
                });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nFailed to generate summary: {ex.Message}");
            }
        }
        
        Console.WriteLine(_formatter.FormatAttachments(message));
    }

    public Task<string> GetEmailContentAsync(MimeMessage message)
    {
        var content = message.TextBody ?? message.HtmlBody ?? string.Empty;
        
        // If content is in HTML, clean it
        if (!string.IsNullOrEmpty(message.HtmlBody))
        {
            content = HtmlExtractor.ExtractText(content);
        }
        
        return Task.FromResult(content);
    }

    public void DisplayProcessedEmailsSummary()
    {
        if (!_processedEmails.Any())
        {
            Console.WriteLine("\nNo emails were processed.");
            return;
        }

        Console.WriteLine("\nProcessed Emails Summary:");
        Console.WriteLine("┌──────────────────────────────────────────────────────────────────────────────────────────────┐");
        Console.WriteLine("│ Date       │ From                     │ Subject                                          │");
        Console.WriteLine("├──────────────────────────────────────────────────────────────────────────────────────────────┤");

        foreach (var email in _processedEmails.OrderByDescending(e => e.Date))
        {
            var date = email.Date.ToString("yyyy-MM-dd");
            var from = $"{email.SenderName} <{email.Sender}>";
            var subject = email.Subject;

            // Truncate long values
            if (from.Length > 25) from = from.Substring(0, 22) + "...";
            if (subject.Length > 45) subject = subject.Substring(0, 42) + "...";

            Console.WriteLine($"│ {date,-10} │ {from,-25} │ {subject,-45} │");
        }

        Console.WriteLine("└──────────────────────────────────────────────────────────────────────────────────────────────┘");
        Console.WriteLine($"Total emails processed: {_processedEmails.Count}");
    }

    private class ProcessedEmailInfo
    {
        public required string Subject { get; set; }
        public required string Sender { get; set; }
        public required string SenderName { get; set; }
        public required DateTime Date { get; set; }
        public required string FilePath { get; set; }
        public required bool HasAttachments { get; set; }
    }
} 