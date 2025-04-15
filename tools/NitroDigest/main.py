import os
from argparse import ArgumentParser
from dotenv import load_dotenv

from email_processor import EmailProcessor
from summarizer import ClaudeSummarizer, ChatGPTSummarizer, OllamaSummarizer, ConfigurationError
from summary_writer import SummaryWriter


def main():
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Define possible program parameters
    parser = ArgumentParser(
        description="NitroDigest - Email newsletter summarizer")
    parser.add_argument("--limit", type=int, default=5,
                        help="Maximum number of emails to process")
    parser.add_argument("--output-dir", default="summaries",
                        help="Directory to save summaries")
    parser.add_argument("--summarizer", choices=["claude", "chatgpt", "ollama"], default="ollama",
                        help="Summarizer to use")
    parser.add_argument("--mark-as-read", action="store_true",
                        help="Mark processed emails as read")
    parser.add_argument("--email", default=os.environ.get("EMAIL_ADDRESS"),
                        help="Email address (overrides environment variable)")
    parser.add_argument("--password", default=os.environ.get("EMAIL_PASSWORD"),
                        help="Email password (overrides environment variable)")
    parser.add_argument("--server", default=os.environ.get("IMAP_SERVER",
                        "imap.gmail.com"), help="IMAP server (overrides environment variable)")
    parser.add_argument("--folder", default="INBOX",
                        help="Email folder to process")
    parser.add_argument("--model", default="",
                        help="Specific model to use (provider-dependent)")

    args = parser.parse_args()

    if not args.email or not args.password:
        print("Email credentials not found. Please provide them as arguments or environment variables.")
        return

    # Initialize components
    email_processor = EmailProcessor(args.email, args.password, args.server)

    # Choose summarizer based on arguments
    try:
        if args.summarizer == "claude":
            api_key = os.environ.get("CLAUDE_API_KEY")
            model = args.model or os.environ.get(
                "CLAUDE_MODEL", "claude-3-haiku-20240307")
            summarizer = ClaudeSummarizer(api_key=api_key, model=model)
        elif args.summarizer == "chatgpt":
            api_key = os.environ.get("OPENAI_API_KEY")
            model = args.model or os.environ.get(
                "OPENAI_MODEL", "gpt-3.5-turbo")
            summarizer = ChatGPTSummarizer(api_key=api_key, model=model)
        elif args.summarizer == "ollama":
            model = args.model or os.environ.get("OLLAMA_MODEL", "mistral")
            base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
            summarizer = OllamaSummarizer(model=model, base_url=base_url)
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error initializing summarizer: {e}")
        return

    summary_writer = SummaryWriter(output_dir=args.output_dir)

    # Process emails
    print(f"Fetching up to {args.limit} unread emails from {args.folder}...")
    emails = email_processor.get_unread_emails(
        folder=args.folder, limit=args.limit)

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
        result = summarizer.summarize(email_data['body'], email_data)

        if not result.is_success():
            print(f"Failed to generate summary: {result.error}")
            continue

        summary = result.summary

        filepath = summary_writer.write_summary(summary, email_data)

        if filepath:
            print(f"Summary saved to: {filepath}")
            print(
                f"Used model: {result.model_used} ({result.tokens_used} tokens)")
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
