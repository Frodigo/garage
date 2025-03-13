namespace Core.Interfaces;

public interface ISummarizer
{
    Task<string> SummarizeAsync(string content, string subject);
} 