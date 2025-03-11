using System;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Linq;
using System.IO;
using System.Text;

public class ClaudeSummarizer : ISummarizer
{
    private readonly string _apiKey;
    private readonly HttpClient _httpClient;

    private const string SYSTEM_PROMPT = @"You are an assistant specializing in analyzing newsletters and creating inspiring summaries. Your task is to:
1. Analyze the content of newsletters for:
   - Unique and valuable information
   - New trends and directions in the industry
   - Interesting statistics and data
   - Potentially viral content
   - Controversial or controversial topics

2. For each valuable information, prepare:
   - Short summary (max 2-3 sentences)
   - Suggestion on how to expand the topic
   - Potential content formats (e.g. article, infographic, analysis)
   - Information source

3. Prioritize information that:
   - Are current and fresh
   - Have potential long-term value
   - May particularly interest recipients
   - Fit current trends

Your answers should be concise and specific, focused on practical use of information.";

    private const string USER_PROMPT_TEMPLATE = @"Analyze the following newsletter and extract the most important information according to the above guidelines:

{0}

Format of the answer:
1. Key information (in order of importance):
   - [Information 1]
   - [Information 2]
   ...

2. Content ideas:
   - [Idea 1]
   - [Idea 2]
   ...

3. Sources to quote:
   - [Source 1]
   - [Source 2]
   ...";

    public ClaudeSummarizer(string apiKey)
    {
        _apiKey = apiKey;
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("https://api.anthropic.com/v1/"),
            Timeout = TimeSpan.FromMinutes(5)
        };
        _httpClient.DefaultRequestHeaders.Add("x-api-key", apiKey);
        _httpClient.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");
    }

    public async Task<string> SummarizeAsync(string text, string emailTitle)
    {
        try
        {
            var request = new
            {
                model = "claude-3-sonnet-20240229",
                max_tokens = 500,
                system = SYSTEM_PROMPT,
                messages = new[]
                {
                    new { role = "user", content = string.Format(USER_PROMPT_TEMPLATE, text) }
                }
            };

            var response = await _httpClient.PostAsJsonAsync("messages", request);
            Console.WriteLine($"Status of the response: {response.StatusCode}");

            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Error content: {errorContent}");
                return $"API error: {response.StatusCode}";
            }

            var responseContent = await response.Content.ReadAsStringAsync();
            var result = await response.Content.ReadFromJsonAsync<ClaudeResponse>();
            var summary = result?.Content?.FirstOrDefault()?.Text ?? "Failed to generate summary.";
            
            await SaveSummaryToFileAsync(summary, emailTitle);
            
            return summary;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error details: {ex}");
            return $"Failed to generate summary: {ex.Message}";
        }
    }

    private async Task SaveSummaryToFileAsync(string summary, string emailTitle)
    {
        var summariesDir = Path.Combine(Directory.GetCurrentDirectory(), "content", "summaries");
        Directory.CreateDirectory(summariesDir);

        // Sanitize email title for file name
        var sanitizedTitle = string.Join("_", emailTitle.Split(Path.GetInvalidFileNameChars()));
        var fileName = $"{sanitizedTitle}_{DateTime.Now:yyyy-MM-dd_HH-mm-ss}.md";
        var filePath = Path.Combine(summariesDir, fileName);

        var frontMatter = $@"---
title: ""{emailTitle}""
date: {DateTime.Now:yyyy-MM-dd HH:mm:ss}
summary_generated: true
model: ""claude-3-sonnet-20240229""
---

";

        var contentWithMetadata = frontMatter + summary;
        await File.WriteAllTextAsync(filePath, contentWithMetadata, Encoding.UTF8);
        Console.WriteLine($"Summary saved to: {filePath}");
    }
}

public class ClaudeResponse
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Role { get; set; }
    public string? Model { get; set; }
    public ClaudeContent[]? Content { get; set; }
}

public class ClaudeContent
{
    public string? Type { get; set; }
    public string? Text { get; set; }
}