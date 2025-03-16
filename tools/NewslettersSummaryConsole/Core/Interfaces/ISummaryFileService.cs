using Core.Models;

namespace Core.Interfaces;

public interface ISummaryFileService
{
    Task SaveSummaryAsync(string subject, string summary, string sender, EmailMetadata metadata);
    string GetSummaryPath(string subject, string sender);
} 