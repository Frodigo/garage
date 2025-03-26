using Core.Services;
using Infrastructure.Email;
using Infrastructure.Summarizers;
using Infrastructure.Files;
using DotNetEnv;
using Core.Interfaces;

Env.Load();

var host = Environment.GetEnvironmentVariable("IMAP_ADDRESS") ?? throw new ArgumentNullException("IMAP_ADDRESS is not set");
var port = int.Parse(Environment.GetEnvironmentVariable("IMAP_PORT") ?? throw new ArgumentNullException("IMAP_PORT is not set"));
var username = Environment.GetEnvironmentVariable("IMAP_USERNAME") ?? throw new ArgumentNullException("IMAP_USERNAME is not set");
var password = Environment.GetEnvironmentVariable("IMAP_PASSWORD") ?? throw new ArgumentNullException("IMAP_PASSWORD is not set");
var summariesPath = Environment.GetEnvironmentVariable("SUMMARIES_PATH") ?? throw new ArgumentNullException("SUMMARIES_PATH is not set");
var activeSummarizer = Environment.GetEnvironmentVariable("ACTIVE_SUMMARIZER") ?? throw new ArgumentNullException("ACTIVE_SUMMARIZER is not set");

var httpClient = new HttpClient();
var connectionManager = new ImapConnectionManager(host, port, username, password);

ISummarizer summarizer = activeSummarizer.ToLower() switch
{
    "claude" => new ClaudeSummarizer(
        Environment.GetEnvironmentVariable("CLAUDE_API_KEY") ?? throw new ArgumentNullException("CLAUDE_API_KEY is not set"),
        httpClient
    ),
    "chatgpt" => new ChatGPTSummarizer(
        Environment.GetEnvironmentVariable("CHATGPT_API_KEY") ?? throw new ArgumentNullException("CHATGPT_API_KEY is not set"),
        httpClient
    ),
    "ollama" => new OllamaSummarizer(
        Environment.GetEnvironmentVariable("OLLAMA_MODEL") ?? throw new ArgumentNullException("OLLAMA_MODEL is not set"),
        httpClient,
        Environment.GetEnvironmentVariable("OLLAMA_API_URL") ?? throw new ArgumentNullException("OLLAMA_API_URL is not set")
    ),
    _ => throw new ArgumentException($"Unknown summarizer type: {activeSummarizer}")
};

var formatter = new EmailFormatter();
var summaryFileService = new SummaryFileService(summariesPath);
var emailProcessor = new EmailProcessor(summarizer, formatter, summaryFileService, activeSummarizer);
var emailService = new EmailService(connectionManager, emailProcessor);

await emailService.ReadUnreadEmails(maxEmails: 1, markAsRead: true);