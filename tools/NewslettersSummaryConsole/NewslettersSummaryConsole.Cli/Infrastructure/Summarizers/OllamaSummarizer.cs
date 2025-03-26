using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Core.Interfaces;
using Infrastructure.Prompts;
using NewslettersSummaryConsole.Core;

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
        Console.WriteLine($"\nProcessing email with subject: {subject}");
        Console.WriteLine($"Original content length: {content.Length} characters");

        // Split text into smaller chunks
        var chunks = TextSplitter.SplitIntoChunks(content);
        Console.WriteLine($"Split into {chunks.Length} chunks");
        
        if (chunks.Length == 1)
        {
            Console.WriteLine("Content is short enough, processing as single chunk");
            return await GenerateSummaryForChunk(chunks[0], subject);
        }

        // For longer texts, generate summaries for each part
        var summaries = new List<string>();
        for (int i = 0; i < chunks.Length; i++)
        {
            Console.WriteLine($"\nProcessing chunk {i + 1}/{chunks.Length}");
            Console.WriteLine($"Chunk length: {chunks[i].Length} characters");
            
            var chunkSummary = await GenerateSummaryForChunk(chunks[i], subject, i + 1, chunks.Length);
            summaries.Add(chunkSummary);
            Console.WriteLine($"Chunk {i + 1} summary length: {chunkSummary.Length} characters");
        }

        Console.WriteLine("\nCombining all summaries...");
        // Combine summaries into one text
        return await CombineSummaries(summaries, subject);
    }

    private async Task<string> GenerateSummaryForChunk(string chunk, string subject, int? partNumber = null, int? totalParts = null)
    {
        var partInfo = partNumber.HasValue && totalParts.HasValue 
            ? $" (Part {partNumber}/{totalParts})" 
            : string.Empty;

        var prompt = EmailSummaryPrompt.GetPrompt(subject, chunk, partInfo);
        Console.WriteLine($"Prompt length: {prompt.Length} characters");

        var request = new
        {
            model = _model,
            prompt = prompt,
            stream = false
        };

        try
        {
            var response = await _httpClient.PostAsync(
                "generate",
                new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json")
            );

            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Error response: {errorContent}");
                throw new Exception($"Ollama API error: {response.StatusCode} - {errorContent}");
            }

            var responseContent = await response.Content.ReadAsStringAsync();
            
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            var responseObject = JsonSerializer.Deserialize<OllamaResponse>(responseContent, options);

            if (responseObject?.Response == null)
            {
                Console.WriteLine("Failed to get response from Ollama");
                return "Failed to generate summary.";
            }

            return responseObject.Response;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Exception during chunk processing: {ex.Message}");
            throw;
        }
    }

    private async Task<string> CombineSummaries(List<string> summaries, string subject)
    {
        var combinedPrompt = $"""
        Combine the following summaries of an email with subject "{subject}" into a single, coherent summary. 
        Maintain the same format and structure as the individual summaries, but ensure the final summary flows naturally and avoids repetition.

        Individual summaries:
        {string.Join("\n\n", summaries)}
        """;

        Console.WriteLine($"Combined prompt length: {combinedPrompt.Length} characters");

        var request = new
        {
            model = _model,
            prompt = combinedPrompt,
            stream = false
        };

        try
        {
            var response = await _httpClient.PostAsync(
                "generate",
                new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json")
            );

            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Error response during combination: {errorContent}");
                throw new Exception($"Ollama API error: {response.StatusCode} - {errorContent}");
            }

            var responseContent = await response.Content.ReadAsStringAsync();
            
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            var responseObject = JsonSerializer.Deserialize<OllamaResponse>(responseContent, options);

            if (responseObject?.Response == null)
            {
                Console.WriteLine("Failed to get response from Ollama during combination");
                return "Failed to combine summaries.";
            }

            return responseObject.Response;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Exception during summary combination: {ex.Message}");
            throw;
        }
    }

    private class OllamaResponse
    {
        [JsonPropertyName("response")]
        public required string Response { get; set; }
    }
} 