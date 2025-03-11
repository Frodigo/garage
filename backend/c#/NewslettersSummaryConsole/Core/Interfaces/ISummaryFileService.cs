namespace Core.Interfaces;

public interface ISummaryFileService
{
    Task SaveSummaryAsync(string subject, string summary);
    string GetSummaryPath(string subject);
} 