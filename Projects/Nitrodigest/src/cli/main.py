from argparse import ArgumentParser
import os
import tempfile
import sys
import yaml
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .summarizer import (
    OllamaSummarizer,
    ConfigurationError
)
from .config import Config

from .summarizer.utils.logging import get_logger

logger = get_logger(__name__)


def main():
    parser = ArgumentParser(
        description="nitrodigest - TLDR text, privately",
        epilog="Visit docs, if you need more information: https://frodigo.com/projects/nitrodigest/docs, or report issues: https://github.com/frodigo/garage/issues if something doesn't work as expected."
    )
    parser.add_argument(
        "content",
        nargs='?',
        help="Text to summarize",
    )
    parser.add_argument(
        "--model",
        default="mistral",
        help="Model to use for summarization (default: mistral)"
    )
    parser.add_argument(
        "--ollama-api-url",
        default="http://localhost:11434",
        help="URL of the local Ollama API (default: http://localhost:11434)"
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
        "--format",
        default="text",
        help="Output format. Can be 'text' or 'json' (default: text)"
    )
    parser.add_argument(
        "--include-original",
        default=False,
        action="store_true",
        help="Include original text in the summary output"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum number of parallel workers for directory processing (default: 4)"
    )

    args = parser.parse_args()

    try:
        temp_prompt_file = None
        if args.prompt:
            temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp.write(args.prompt)
            temp.close()
            temp_prompt_file = temp.name

        config = Config(
            model=args.model,
            ollama_api_url=args.ollama_api_url,
            timeout=args.timeout,
            prompt_file=temp_prompt_file
        )

    except Exception as e:
        print(f"Configuration error: {e}")
        return -1

    try:
        summarizer = OllamaSummarizer(
            model=config.model,
            ollama_api_url=config.ollama_api_url,
            timeout=config.timeout,
            prompt_file=config.prompt_file
        )
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return -1
    except Exception as e:
        logger.error(f"Unexpected error initializing summarizer: {e}")
        return -1

    if not sys.stdin.isatty():
        content = sys.stdin.read()
        process_text(content, summarizer, args.format, args.include_original)
    elif not args.content:
        current_dir = os.getcwd()
        process_directory(current_dir, summarizer,
                          args.format, args.include_original, args.max_workers)

    else:
        if os.path.isfile(args.content):
            process_file(args.content, summarizer,
                         args.format, args.include_original)
        elif os.path.isdir(args.content):
            process_directory(args.content, summarizer,
                              args.format, args.include_original, args.max_workers)
        else:
            process_text(args.content, summarizer,
                         args.format, args.include_original)

    # Clean up a temporary prompt file if it was created
    if (args.prompt and config.prompt_file and
            os.path.exists(config.prompt_file)):
        os.remove(config.prompt_file)

    return 0


def process_text(content: str, summarizer: OllamaSummarizer, format: str, include_original: bool) -> int:
    try:
        logger.info("Processing text...")

        metadata = {
            "title": f"{content[:30]}...",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "text"
        }

        return _generate_summary(content, summarizer, metadata, format, include_original)

    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return -1


def process_file(file_path, summarizer, format: str, include_original: bool):
    """Process a single file for summarization and print results"""
    try:
        logger.info(f"Processing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            logger.warning(f"Warning: File '{file_path}' is empty")
            return -1

        file_name = os.path.basename(file_path)
        metadata = {
            'title': file_name,
            'source': 'file://' + os.path.abspath(file_path),
            'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
            'id': file_path
        }

        logger.info(f"Generating summary for {file_name}...")
        return _generate_summary(content, summarizer, metadata, format, include_original)

    except Exception:
        raise


def _process_file_return_result(file_path, summarizer, format: str, include_original: bool):
    """Process a single file and return the result without printing"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            return None

        file_name = os.path.basename(file_path)
        metadata = {
            'title': file_name,
            'source': 'file://' + os.path.abspath(file_path),
            'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
            'id': file_path
        }

        result = summarizer.summarize(content, metadata)

        if not result.is_success():
            return None

        return {
            'content': content,
            'metadata': metadata,
            'summary': result.summary,
            'model_used': result.model_used,
            'tokens_used': result.tokens_used,
            'file_path': file_path
        }

    except Exception:
        raise


def process_directory(directory_path, summarizer, format: str, include_original: bool, max_workers: int = 4):
    """Process all text files in a directory with parallel processing and progress tracking"""

    files_to_process = []
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.lower().endswith(('.txt', '.md', '.html', '.htm', '.xml', '.json', '.csv', '.log')):
                file_path = os.path.join(root, filename)
                files_to_process.append(file_path)

    file_count = len(files_to_process)

    if file_count == 0:
        print("No text files found to process")
        return

    print(f"\nProcessing directory: {directory_path}")
    print(f"Found {file_count} files to process with {max_workers} workers\n")

    import logging
    original_levels = {}
    for log_name in ['cli.summarizer.base.OllamaSummarizer', 'cli.main']:
        log = logging.getLogger(log_name)
        original_levels[log_name] = log.level
        log.setLevel(logging.WARNING)

    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(_process_file_return_result, file_path, summarizer, format, include_original): file_path
            for file_path in files_to_process
        }

        with tqdm(
            total=file_count,
            desc="Processing",
            unit="file",
            bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
            leave=True,
            position=0
        ) as pbar:
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                file_name = os.path.basename(file_path)

                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        pbar.set_postfix_str(
                            f"✓ {file_name[:50]}", refresh=True)
                    else:
                        errors.append(
                            (file_path, "Empty file or failed to generate summary"))
                        pbar.set_postfix_str(
                            f"✗ {file_name[:50]}", refresh=True)
                except Exception as e:
                    errors.append((file_path, str(e)))
                    pbar.set_postfix_str(f"✗ {file_name[:50]}", refresh=True)
                finally:
                    pbar.update(1)

    for log_name, level in original_levels.items():
        logging.getLogger(log_name).setLevel(level)

    print(
        f"\nProcessing complete: {len(results)} successful, {len(errors)} failed\n")

    if errors:
        print("Failed files:")
        for file_path, error in errors:
            print(f"  - {os.path.basename(file_path)}: {error}")
        print()

    for idx, result in enumerate(results, 1):
        _print_result(result, format, include_original)
        if idx < len(results):
            print("\n" + "=" * 80 + "\n")


def _print_result(result, format: str, include_original: bool):
    """Print a single result"""
    metadata = result['metadata']
    summary = result['summary']
    content = result['content']

    if format == 'text':
        print('---')
        yaml.dump(
            {
                'title': metadata.get('title', 'Untitled'),
                'source': metadata.get('source', 'Unknown'),
                'date': metadata.get('date', datetime.now().strftime("%Y-%m-%d")),
                'id': metadata.get('id', ''),
                'summary_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'model': result['model_used'],
                'tokens': result['tokens_used']
            },
            sys.stdout,
            default_flow_style=False,
            allow_unicode=True
        )
        print('---\n')
        print(_json_to_text(summary))

        if include_original:
            print("\n---\n")
            print("## Original Text\n")
            print(content)
    elif format == 'json':
        json_summary = json.loads(summary)
        json_summary["metadata"] = metadata
        json_summary["model_used"] = result['model_used']
        json_summary["tokens_used"] = result['tokens_used']

        if include_original:
            json_summary["original_text"] = content

        print(json.dumps(json_summary, ensure_ascii=False, indent=2))
    else:
        print(summary)


def _generate_summary(content, summarizer, metadata, format, include_original=True) -> int:
    result = summarizer.summarize(content, metadata)

    if not result.is_success():
        logger.error(
            f"Failed to generate summary: {result.error}")
        return -1

    summary = result.summary

    if format == 'text':
        print('---')
        yaml.dump(
            {
                'title': metadata.get('title', 'Untitled'),
                'source': metadata.get('source', 'Unknown'),
                'date': metadata.get('date', datetime.now().strftime("%Y-%m-%d")),
                'id': metadata.get('id', ''),
                'summary_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'model': result.model_used,
                'tokens': result.tokens_used
            },
            sys.stdout,
            default_flow_style=False,
            allow_unicode=True
        )
        print('---\n')
        print(_json_to_text(summary))

        if include_original:
            print("\n---\n")
            print("## Original Text\n")
            print(content)
    elif format == 'json':
        json_summary = json.loads(summary)
        json_summary["metadata"] = metadata

        if include_original:
            json_summary["original_text"] = content

        print(json.dumps(json_summary, ensure_ascii=False, indent=2))
    else:
        print(summary)
    return 0


def _json_to_text(json_data):
    """Convert JSON data to formatted text with headings and ordered lists."""

    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    result = []

    for key, value in data.items():
        heading = key.capitalize()
        result.append(f"# {heading}\n")

        if isinstance(value, list):
            for i, item in enumerate(value, 1):
                result.append(f"{i}. {item}")
        else:
            result.append(f"{value}")

        result.append("")

    return "\n".join(result).strip()


if __name__ == "__main__":
    main()
