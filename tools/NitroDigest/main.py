from argparse import ArgumentParser
import os

from email_processor import EmailProcessor
from summarizer import (
    ClaudeSummarizer,
    ChatGPTSummarizer,
    OllamaSummarizer,
    ConfigurationError
)
from summary_writer import SummaryWriter
from config import Config, SummarizerType


def main():
    # Define possible program parameters
    parser = ArgumentParser(
        description="NitroDigest - Email newsletter summarizer"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to JSON configuration file (default: config.json)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of emails to process"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save summaries"
    )
    parser.add_argument(
        "--mark-as-read",
        action="store_true",
        help="Mark processed emails as read"
    )
    parser.add_argument(
        "--email",
        help="Email address (overrides config)"
    )
    parser.add_argument(
        "--password",
        help="Email password (overrides config)"
    )
    parser.add_argument(
        "--server",
        help="IMAP server (overrides config)"
    )
    parser.add_argument(
        "--folder",
        help="Email folder to process"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for API requests"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        if not os.path.exists(args.config):
            print(f"Error: Configuration file '{args.config}' not found")
            return

        config = Config.from_json(args.config)

        # Override config with command line arguments if provided
        if args.limit:
            config.limit = args.limit
        if args.output_dir:
            config.summaries_path = args.output_dir
        if args.mark_as_read:
            config.mark_as_read = True
        if args.email:
            config.email.address = args.email
        if args.password:
            config.email.password = args.password
        if args.server:
            config.email.server = args.server
        if args.folder:
            config.email.folder = args.folder
        if args.timeout:
            config.summarizer.timeout = args.timeout

        # Validate configuration
        config.validate()

    except Exception as e:
        print(f"Configuration error: {e}")
        return

    # Initialize components
    email_processor = EmailProcessor(
        config.email.address,
        config.email.password,
        config.email.server,
        config.email.port
    )

    # Choose summarizer based on configuration
    try:
        if config.summarizer.type == SummarizerType.CLAUDE:
            if not config.summarizer.api_key:
                raise ConfigurationError("Claude API key is required")
            if not config.summarizer.model:
                raise ConfigurationError("Model is required for Claude")
            summarizer = ClaudeSummarizer(
                api_key=config.summarizer.api_key,
                model=config.summarizer.model,
                timeout=config.summarizer.timeout
            )
        elif config.summarizer.type == SummarizerType.CHATGPT:
            if not config.summarizer.api_key:
                raise ConfigurationError("ChatGPT API key is required")
            if not config.summarizer.model:
                raise ConfigurationError("Model is required for ChatGPT")
            summarizer = ChatGPTSummarizer(
                api_key=config.summarizer.api_key,
                model=config.summarizer.model,
                timeout=config.summarizer.timeout
            )
        elif config.summarizer.type == SummarizerType.OLLAMA:
            if not config.summarizer.model:
                raise ConfigurationError("Model is required for Ollama")
            summarizer = OllamaSummarizer(
                model=config.summarizer.model,
                base_url=config.summarizer.base_url,
                timeout=config.summarizer.timeout
            )
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error initializing summarizer: {e}")
        return

    summary_writer = SummaryWriter(output_dir=config.summaries_path)

    # Process emails
    print(
        f"Fetching up to {config.limit} unread emails from "
        f"{config.email.folder}..."
    )
    emails = email_processor.get_unread_emails(
        folder=config.email.folder, limit=config.limit)

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
                f"Used model: {result.model_used} "
                f"({result.tokens_used} tokens)"
            )
        else:
            print("Failed to save summary.")

        # Mark as read if requested
        if config.mark_as_read:
            email_processor.mark_as_read(email_data['id'])
            print("Email marked as read")

    # Disconnect from email server
    email_processor.disconnect()
    print("\nAll emails processed.")


if __name__ == "__main__":
    main()
