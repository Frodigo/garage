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

    public EmailProcessor(ISummarizer summarizer, IEmailFormatter formatter, ISummaryFileService summaryFileService, string activeSummarizer)
    {
        _summarizer = summarizer;
        _formatter = formatter;
        _summaryFileService = summaryFileService;
        _activeSummarizer = activeSummarizer;
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
                await _summaryFileService.SaveSummaryAsync(message.Subject!, summary, content, metadata.Sender, metadata);
                Console.WriteLine($"Summary saved to: {_summaryFileService.GetSummaryPath(message.Subject!, metadata.Sender)}");
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
} 