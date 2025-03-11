using Core.Services;
using Infrastructure.Email;
using Infrastructure.Summarizers;
using Infrastructure.Files;
using DotNetEnv;

Env.Load();

var host = Environment.GetEnvironmentVariable("IMAP_ADDRESS") ?? throw new ArgumentNullException("IMAP_ADDRESS is not set");
var port = int.Parse(Environment.GetEnvironmentVariable("IMAP_PORT") ?? throw new ArgumentNullException("IMAP_PORT is not set"));
var username = Environment.GetEnvironmentVariable("IMAP_USERNAME") ?? throw new ArgumentNullException("IMAP_USERNAME is not set");
var password = Environment.GetEnvironmentVariable("IMAP_PASSWORD") ?? throw new ArgumentNullException("IMAP_PASSWORD is not set");
var summariesPath = Environment.GetEnvironmentVariable("SUMMARIES_PATH") ?? throw new ArgumentNullException("SUMMARIES_PATH is not set");

var httpClient = new HttpClient();
var connectionManager = new ImapConnectionManager(host, port, username, password);
var summarizer = new ClaudeSummarizer(Environment.GetEnvironmentVariable("CLAUDE_API_KEY") ?? throw new ArgumentNullException("CLAUDE_API_KEY is not set"), httpClient);
var formatter = new EmailFormatter();
var summaryFileService = new SummaryFileService(summariesPath);
var emailProcessor = new EmailProcessor(summarizer, formatter, summaryFileService);
var emailService = new EmailService(connectionManager, emailProcessor);

await emailService.ReadUnreadEmails(maxEmails: 5, markAsRead: true);