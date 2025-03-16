namespace Core.Models;

public class EmailMetadata
{
    public required string Subject { get; set; }
    public required string Sender { get; set; }
    public required string SenderName { get; set; }
    public required DateTime Date { get; set; }
    public required string Summarizer { get; set; }
    public required string Recipients { get; set; }
    public bool HasAttachments { get; set; }
} 