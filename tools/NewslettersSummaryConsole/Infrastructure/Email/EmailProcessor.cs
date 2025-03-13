using Core.Interfaces;
using MimeKit;

namespace Infrastructure.Email;

public class EmailProcessor : IEmailProcessor
{
    private readonly ISummarizer _summarizer;
    private readonly IEmailFormatter _formatter;
    private readonly ISummaryFileService _summaryFileService;

    public EmailProcessor(ISummarizer summarizer, IEmailFormatter formatter, ISummaryFileService summaryFileService)
    {
        _summarizer = summarizer;
        _formatter = formatter;
        _summaryFileService = summaryFileService;
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
                
                // Save summary to file
                await _summaryFileService.SaveSummaryAsync(message.Subject, summary);
                Console.WriteLine($"Summary saved to: {_summaryFileService.GetSummaryPath(message.Subject)}");
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
        return Task.FromResult(message.TextBody ?? message.HtmlBody ?? string.Empty);
    }
} 