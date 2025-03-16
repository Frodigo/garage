using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Core.Interfaces;
using Infrastructure.Prompts;

namespace Infrastructure.Summarizers;

public class OllamaSummarizer : ISummarizer
{
    private readonly HttpClient _httpClient;
    private readonly string _model;

    public OllamaSummarizer(string model, HttpClient httpClient, string apiUrl)
    {
        _model = model;
        _httpClient = httpClient;
        _httpClient.BaseAddress = new Uri($"{apiUrl}/api/");
    }

    public async Task<string> SummarizeAsync(string content, string subject)
    {
        var prompt = EmailSummaryPrompt.GetPrompt(subject, content);

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
        
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };

        var responseObject = JsonSerializer.Deserialize<OllamaResponse>(responseContent, options);

        if (responseObject?.Response == null)
        {
            return "Failed to generate summary.";
        }

        return responseObject.Response;
    }

    private class OllamaResponse
    {
        [JsonPropertyName("response")]
        public required string Response { get; set; }
    }
} 