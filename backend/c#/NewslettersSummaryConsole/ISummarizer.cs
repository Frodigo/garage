public interface ISummarizer
{
    Task<string> SummarizeAsync(string text, string emailTitle);
}