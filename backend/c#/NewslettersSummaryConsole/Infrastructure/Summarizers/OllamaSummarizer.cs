using System.Text;
using System.Text.Json;
using Core.Interfaces;

namespace Infrastructure.Summarizers;

public class OllamaSummarizer : ISummarizer
{
    private readonly HttpClient _httpClient;
    private readonly string _model;

    public OllamaSummarizer(string model = "mistral")
    {
        _model = model;
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("http://localhost:11434/api/")
        };
    }

    public async Task<string> SummarizeAsync(string content, string subject)
    {
        var prompt = $"Summarize the following email with subject '{subject}' in English. Focus on the most important information and key points:\n\n{content}";

        var request = new
        {
            model = _model,
            prompt = prompt,
            stream = false
        };

        var response = await _httpClient.PostAsync(
            "generate",
            new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json")
        );

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"Ollama API error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}");
        }

        var responseContent = await response.Content.ReadAsStringAsync();
        var responseObject = JsonSerializer.Deserialize<OllamaResponse>(responseContent);

        return responseObject?.Response ?? "Failed to generate summary.";
    }

    private class OllamaResponse
    {
        public required string Response { get; set; }
    }
} 