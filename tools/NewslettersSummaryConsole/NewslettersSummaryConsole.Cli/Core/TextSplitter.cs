namespace NewslettersSummaryConsole.Core;

public static class TextSplitter
{
    private const int MaxTokensPerChunk = 1500; 
    private const int MaxCharactersPerChunk = 1000;
    private const int PromptOverhead = 500;

    public static string[] SplitIntoChunks(string text)
    {
        Console.WriteLine($"\nStarting text splitting process");
        Console.WriteLine($"Input text length: {text.Length} characters");

        var chunks = new List<string>();
        var words = text.Split(new[] { ' ', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
        var currentChunk = new List<string>();
        var currentLength = 0;
        var chunkCount = 0;

        foreach (var word in words)
        {
            var wordLength = word.Length + 1; // +1 for space

            if (currentLength + wordLength + PromptOverhead > MaxCharactersPerChunk)
            {
                // Save current chunk
                var chunk = string.Join(" ", currentChunk);
                if (!string.IsNullOrWhiteSpace(chunk))
                {
                    chunks.Add(chunk);
                    Console.WriteLine($"Created chunk {++chunkCount} with {chunk.Length} characters");
                }

                // Start new chunk
                currentChunk.Clear();
                currentLength = 0;
            }

            currentChunk.Add(word);
            currentLength += wordLength;
        }

        // Add the last chunk if it's not empty
        if (currentChunk.Any())
        {
            var chunk = string.Join(" ", currentChunk);
            if (!string.IsNullOrWhiteSpace(chunk))
            {
                chunks.Add(chunk);
                Console.WriteLine($"Created chunk {++chunkCount} with {chunk.Length} characters");
            }
        }

        Console.WriteLine($"Total chunks created: {chunks.Count}");
        return chunks.ToArray();
    }

    private static string[] SplitIntoSentences(string text)
    {
        // Split text into sentences using common sentence endings
        var sentences = text.Split(new[] { 
            ". ", 
            "! ", 
            "? ",
            ".\n",
            "!\n",
            "?\n",
            ".\r\n",
            "!\r\n",
            "?\r\n"
        }, StringSplitOptions.RemoveEmptyEntries)
        .Select(s => s.Trim())
        .Where(s => !string.IsNullOrWhiteSpace(s))
        .ToArray();

        // Group sentences into chunks of 3-4 sentences
        var groupedSentences = new List<string>();
        var currentGroup = new List<string>();

        foreach (var sentence in sentences)
        {
            currentGroup.Add(sentence);
            if (currentGroup.Count >= 4)
            {
                groupedSentences.Add(string.Join(" ", currentGroup));
                currentGroup.Clear();
            }
        }

        if (currentGroup.Any())
        {
            groupedSentences.Add(string.Join(" ", currentGroup));
        }

        return groupedSentences.ToArray();
    }
} 