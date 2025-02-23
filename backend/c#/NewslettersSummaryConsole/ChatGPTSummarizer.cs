using System;
using System.Net.Http.Json;
using System.Threading.Tasks;

public class ChatGPTSummarizer : ISummarizer
{
    private readonly string _apiKey;
    private readonly HttpClient _httpClient;

    public ChatGPTSummarizer(string apiKey)
    {
        _apiKey = apiKey;
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("https://api.openai.com/v1/"),
            Timeout = TimeSpan.FromMinutes(5)
        };
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
    }

    public async Task<string> SummarizeAsync(string text)
    {
        try 
        {
            var request = new
            {
                model = "gpt-4o-mini",
                messages = new[]
                {
                    new
                    {
                        role = "system",
                        content = "Summarize the text in Polish."
                    },
                    new
                    {
                        role = "user",
                        content = text
                    }
                },
                temperature = 0.7,
                max_tokens = 500  // adding a limit of tokens
            };

            for (int i = 0; i < 3; i++) // trying 3 times
            {
                try
                {
                    var response = await _httpClient.PostAsJsonAsync("chat/completions", request);
                    
                    Console.WriteLine($"Status of the response: {response.StatusCode}");
                    
                    if (!response.IsSuccessStatusCode)
                    {
                        var errorContent = await response.Content.ReadAsStringAsync();
                        Console.WriteLine($"Error content: {errorContent}");
                    }
                    
                    response.EnsureSuccessStatusCode();
                    
                    var result = await response.Content.ReadFromJsonAsync<ChatGPTResponse>();
                    return result?.Choices?[0]?.Message?.Content ?? "Failed to generate summary.";
                }
                catch (HttpRequestException ex)
                {
                    Console.WriteLine($"Attempt {i + 1} failed: {ex.Message}");
                    if (i < 2) // if it's not the last attempt
                    {
                        await Task.Delay(2000 * (i + 1)); // increasing the waiting time with each attempt
                        continue;
                    }
                    throw;
                }
            }
            
            return "Failed to generate summary after 3 attempts.";
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error details: {ex}");
            return $"Failed to generate summary: {ex.Message}";
        }
    }
}

public class ChatGPTResponse
{
    public Choice[] Choices { get; set; }
}

public class Choice
{
    public Message Message { get; set; }
}

public class Message
{
    public string Content { get; set; }
} 