using System.Text;
using System.Text.Json;
using System.Net.Http;

public class OllamaSummarizer
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    private readonly string _model;

    public OllamaSummarizer(string baseUrl = "http://localhost:11434", string model = "llama3.3")
    {
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromMinutes(5)
        };
        _baseUrl = baseUrl;
        _model = model;
    }

    public async Task<string> SummarizeText(string text)
    {
        var prompt = $"Summarize the following text in 2-3 sentences in Polish:\n\n{text}";

        var request = new
        {
            model = _model,
            prompt = prompt,
            stream = false
        };


        var response = await _httpClient.PostAsync(
            $"{_baseUrl}/api/generate",
            new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json")
        );

        var content = await response.Content.ReadAsStringAsync();
        var result = JsonSerializer.Deserialize<OllamaResponse>(content);
        Console.WriteLine($"result: {result}");
        return result?.Response ?? "Failed to generate summary.";
    }

    private class OllamaResponse
    {
        public string? Response { get; set; }
    }
}