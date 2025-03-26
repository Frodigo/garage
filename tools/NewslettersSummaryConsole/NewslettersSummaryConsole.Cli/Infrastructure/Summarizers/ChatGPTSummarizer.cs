using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Core.Interfaces;
using Infrastructure.Prompts;

namespace Infrastructure.Summarizers;

public class ChatGPTSummarizer : ISummarizer
{
    private readonly HttpClient _httpClient;

    public ChatGPTSummarizer(string apiKey, HttpClient httpClient)
    {
        _httpClient = httpClient;
        _httpClient.BaseAddress = new Uri("https://api.openai.com/v1/");
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
    }

    public async Task<string> SummarizeAsync(string content, string subject)
    {
        var prompt = EmailSummaryPrompt.GetPrompt(subject, content);

        var request = new
        {
            model = "gpt-4-turbo-preview",
            messages = new[]
            {
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
        
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };

        var responseObject = JsonSerializer.Deserialize<ChatGPTResponse>(responseContent, options);

        if (responseObject?.Choices == null || responseObject.Choices.Length == 0 || responseObject.Choices[0].Message?.Content == null)
        {
            return "Failed to generate summary.";
        }

        return responseObject.Choices[0].Message.Content;
    }

    private class ChatGPTResponse
    {
        [JsonPropertyName("choices")]
        public required Choice[] Choices { get; set; }

        public class Choice
        {
            [JsonPropertyName("message")]
            public required Message Message { get; set; }
        }

        public class Message
        {
            [JsonPropertyName("content")]
            public required string Content { get; set; }
        }
    }
} 