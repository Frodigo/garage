using System.Text;
using System.Text.Json;
using Core.Interfaces;

namespace Infrastructure.Summarizers;

public class ChatGPTSummarizer : ISummarizer
{
    private readonly string _apiKey;
    private readonly HttpClient _httpClient;

    public ChatGPTSummarizer(string apiKey)
    {
        _apiKey = apiKey;
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("https://api.openai.com/v1/")
        };
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_apiKey}");
    }

    public async Task<string> SummarizeAsync(string content, string subject)
    {
        var prompt = $"Summarize the following email with subject '{subject}' in English. Focus on the most important information and key points:\n\n{content}";

        var request = new
        {
            model = "gpt-4-turbo-preview",
            messages = new[]
            {
                new
                {
                    role = "system",
                    content = "You are a helpful assistant who summarizes emails in English."
                },
                new
                {
                    role = "user",
                    content = prompt
                }
            },
            max_tokens = 1000
        };

        var response = await _httpClient.PostAsync(
            "chat/completions",
            new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json")
        );

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"ChatGPT API error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}");
        }

        var responseContent = await response.Content.ReadAsStringAsync();
        var responseObject = JsonSerializer.Deserialize<ChatGPTResponse>(responseContent);

        return responseObject?.Choices?[0]?.Message?.Content ?? "Failed to generate summary.";
    }

    private class ChatGPTResponse
    {
        public required Choice[] Choices { get; set; }

        public class Choice
        {
            public required Message Message { get; set; }
        }

        public class Message
        {
            public required string Content { get; set; }
        }
    }
} 