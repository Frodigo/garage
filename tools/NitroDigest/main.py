import os
import argparse
from dotenv import load_dotenv

from email_processor import EmailProcessor
from summarizer import ClaudeSummarizer, ChatGPTSummarizer, OllamaSummarizer
from summary_writer import SummaryWriter


def main():
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NitroDigest - Email newsletter summarizer")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of emails to process")
    parser.add_argument("--output-dir", default="summaries", help="Directory to save summaries")
    parser.add_argument("--summarizer", choices=["claude", "chatgpt", "ollama"], default="ollama", 
                        help="Summarizer to use")
    parser.add_argument("--mark-as-read", action="store_true", help="Mark processed emails as read")
    parser.add_argument("--email", help="Email address (overrides environment variable)")
    parser.add_argument("--password", help="Email password (overrides environment variable)")
    parser.add_argument("--server", help="IMAP server (overrides environment variable)")
    parser.add_argument("--folder", default="INBOX", help="Email folder to process")
    
    args = parser.parse_args()
    
    # Get email credentials
    email_address = args.email or os.environ.get("EMAIL_ADDRESS")
    password = args.password or os.environ.get("EMAIL_PASSWORD")
    imap_server = args.server or os.environ.get("IMAP_SERVER", "imap.gmail.com")
    
    if not email_address or not password:
        print("Email credentials not found. Please provide them as arguments or environment variables.")
        return
    
    # Initialize components
    email_processor = EmailProcessor(email_address, password, imap_server)
    
    # Choose summarizer based on arguments
    if args.summarizer == "claude":
        api_key = os.environ.get("CLAUDE_API_KEY")
        if not api_key:
            print("Claude API key not found in environment variables")
            return
        summarizer = ClaudeSummarizer(api_key)
    elif args.summarizer == "chatgpt":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("OpenAI API key not found in environment variables")
            return
        summarizer = ChatGPTSummarizer(api_key)
    elif args.summarizer == "ollama":
        model = os.environ.get("OLLAMA_MODEL", "mistral")
        base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        summarizer = OllamaSummarizer(model, base_url)
    
    summary_writer = SummaryWriter(output_dir=args.output_dir)
    
    # Process emails
    print(f"Fetching up to {args.limit} unread emails from {args.folder}...")
    emails = email_processor.get_unread_emails(folder=args.folder, limit=args.limit)
    
    if not emails:
        print("No unread emails found.")
        return
    
    print(f"Found {len(emails)} unread emails. Processing...")
    
    for i, email_data in enumerate(emails):
        print(f"\nProcessing email {i+1}/{len(emails)}:")
        print(f"Subject: {email_data['subject']}")
        print(f"From: {email_data['from']}")
        
        # Summarize
        print("Generating summary...")
        summary = summarizer.summarize(email_data['body'], email_data)
        
        if not summary:
            print("Failed to generate summary. Skipping...")
            continue
        
        # Write summary to file
        filepath = summary_writer.write_summary(summary, email_data)
        
        if filepath:
            print(f"Summary saved to: {filepath}")
        else:
            print("Failed to save summary.")
        
        # Mark as read if requested
        if args.mark_as_read:
            email_processor.mark_as_read(email_data['id'])
            print("Email marked as read")
    
    # Disconnect from email server
    email_processor.disconnect()
    print("\nAll emails processed.")


if __name__ == "__main__":
    main()
