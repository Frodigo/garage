using Core.Interfaces;
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

    public async Task SaveSummaryAsync(string subject, string summary)
    {
        var filePath = GetSummaryPath(subject);
        await File.WriteAllTextAsync(filePath, summary);
    }

    public string GetSummaryPath(string subject)
    {
        var sanitizedSubject = SanitizeFileName(subject);
        return Path.Combine(_summariesPath, $"{sanitizedSubject}_{DateTime.Now:yyyy-MM-dd_HH-mm-ss}.md");
    }

    private static string SanitizeFileName(string fileName)
    {
        // Remove invalid characters from the filename
        var invalidChars = Regex.Escape(new string(Path.GetInvalidFileNameChars()));
        var invalidRegEx = string.Format(@"([{0}]*\.+$)|([{0}]+)", invalidChars);
        
        return Regex.Replace(fileName, invalidRegEx, "_");
    }
} 