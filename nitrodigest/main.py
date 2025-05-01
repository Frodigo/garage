from argparse import ArgumentParser
import os
import tempfile
from datetime import datetime

from summarizer import (
    OllamaSummarizer,
    ConfigurationError
)
from summary_writer import SummaryWriter
from config import Config


def main():
    parser = ArgumentParser(
        description="nitrodigest - TLDR text, privately"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to JSON configuration file (default: config.json)"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save summaries"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout in seconds for API requests to Ollama (default: 300)"
    )
    parser.add_argument(
        "--prompt-file",
        help="Path to custom prompt template file (overrides config)"
    )
    parser.add_argument(
        "--prompt",
        help="Direct prompt content (overrides both config and prompt-file)"
    )
    parser.add_argument(
        "--input",
        help="Path to a single file or directory to summarize"
    )

    args = parser.parse_args()

    if args.input and not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        return -1

    try:
        if not os.path.exists(args.config):
            print(f"Error: Configuration file '{args.config}' not found")
            return -1

        config = Config.from_json(args.config)

        if args.output_dir:
            config.summaries_path = args.output_dir

        if args.timeout:
            config.timeout = args.timeout
        if args.prompt_file:
            config.prompt_file = args.prompt_file
        if args.prompt:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(args.prompt)
                config.prompt_file = f.name

        config.validate()

    except Exception as e:
        print(f"Configuration error: {e}")
        return -1

    try:
        if not config.model:
            raise ConfigurationError("Model is required for Ollama")

        summarizer = OllamaSummarizer(
            model=config.model,
            ollama_api_url=config.ollama_api_url,
            timeout=config.timeout,
            prompt_file=config.prompt_file
        )
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error initializing summarizer: {e}")
        return -1

    summary_writer = SummaryWriter(output_dir=config.summaries_path)

    # Handle input file or directory
    if args.input:
        if os.path.isfile(args.input):
            process_file(args.input, summarizer, summary_writer)
        elif os.path.isdir(args.input):
            process_directory(args.input, summarizer, summary_writer)
        else:
            print(f"Error: '{args.input}' is neither a file nor a directory")
            return -1
    else:
        print("Error: No input file or directory specified. Use --input to specify a file or directory to summarize.")
        return -1

    # Clean up temporary prompt file if it was created
    if (args.prompt and config.prompt_file and
            os.path.exists(config.prompt_file)):
        os.remove(config.prompt_file)
        print("Cleaned up temporary prompt file.")


def process_file(file_path, summarizer, summary_writer):
    """Process a single file for summarization"""
    try:
        print(f"Processing file: {file_path}")

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            print(f"Warning: File '{file_path}' is empty")
            return

        # Create metadata from file info
        file_name = os.path.basename(file_path)
        metadata = {
            'subject': file_name,
            'from': 'file://' + os.path.abspath(file_path),
            'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
            'id': file_path
        }

        # Generate summary
        print(f"Generating summary for {file_name}...")
        result = summarizer.summarize(content, metadata)

        if not result.is_success():
            print(f"Failed to generate summary: {result.error}")
            return -1

        summary = result.summary
        filepath = summary_writer.write_summary(summary, metadata)

        if filepath:
            print(f"Summary saved to: {filepath}")
            print(
                f"Used model: {result.model_used} "
                f"({result.tokens_used} tokens)"
            )
        else:
            print("Failed to save summary.")

    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")


def process_directory(directory_path, summarizer, summary_writer):
    """Process all text files in a directory for summarization"""
    print(f"Processing directory: {directory_path}")

    # Get all files in directory
    file_count = 0
    success_count = 0

    for root, _, files in os.walk(directory_path):
        for filename in files:
            # Only process text files - check common text file extensions
            if filename.lower().endswith(('.txt', '.md', '.html', '.htm', '.xml', '.json', '.csv', '.log')):
                file_path = os.path.join(root, filename)
                try:
                    process_file(file_path, summarizer, summary_writer)
                    success_count += 1
                except Exception as e:
                    print(f"Error processing '{file_path}': {e}")
                file_count += 1

    print(
        f"Directory processing complete: {success_count} of {file_count} files processed successfully")


if __name__ == "__main__":
    main()
