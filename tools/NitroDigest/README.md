# NitroDigest

A Python tool for automatically summarizing email newsletters using AI.

## Features

- Connect to IMAP email servers to retrieve unread newsletters
- Extract text content from HTML emails
- Summarize content using various AI models:
  - Claude (Anthropic)
  - ChatGPT (OpenAI)
  - Ollama (local models)
- Save summaries as Markdown files with YAML frontmatter
- Command-line interface with various options

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

```bash
# Clone the repository
git clone https://github.com/Frodigo/garage
cd tools/NitroDigest
```

### Create a virtual environment

### Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Using conda

```bash
# Create conda environment
conda create -n nitrodigest python=3.11

# Activate environment
conda activate nitrodigest
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project directory with the following variables:

```bash
# Email credentials (required)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-password-or-app-password
IMAP_SERVER=imap.gmail.com

# AI API keys (at least one is required)
ANTHROPIC_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key

# Ollama configuration (if you prefer to use ollama)
OLLAMA_MODEL=mistral
OLLAMA_URL=http://localhost:11434
```

### Gmail Configuration

If you're using Gmail, you'll need to:

1. Enable IMAP in your Gmail settings. For personal accounts it is enabled already, and this option is not visible in settings.
2. Create an app password if you have 2-factor authentication enabled, or if your regular password is not working, and you get authentication errors when attempting to use NitroDigest.
    - Go to [app passwords settings](https://myaccount.google.com/apppasswords).
    - Add new "app" with whatever name you want, then generate the 16-character password. This password can now be used instead of your regular password.

## Usage

### Basic Usage

```bash
# Process 5 unread emails using Claude (default)
python main.py
```

### Command Line Options

```bash
# Process 10 unread emails
python main.py --limit 10

# Use ChatGPT instead of Claude
python main.py --summarizer chatgpt

# Process emails from a specific folder
python main.py --folder "Newsletters"

# Save summaries to a custom directory
python main.py --output-dir "my_summaries"

# Use local Ollama model
python main.py --summarizer ollama

# Mark processed emails as read
python main.py --mark-as-read

# See all available options
python main.py --help
```

### Output

The program will create markdown files in the specified output directory (default: `summaries/`). Each summary file includes:

- YAML frontmatter with metadata
- Markdown-formatted summary of the newsletter content
- Files are named using the date and subject of the email

## Testing

### Running Tests

Run all tests:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=.
```

### Test Organization

- Tests are located in the `__tests__` directory
- Each module has a corresponding test file with the naming convention `test_*.py`
- Test discovery is configured in `pytest.ini`

### Running Specific Tests

```bash
# Run a specific test file
python -m pytest __tests__/test_html_extractor.py

# Run a specific test class
python -m pytest __tests__/test_summarizer.py::TestClaudeSummarizer

# Run a specific test method
python -m pytest __tests__/test_summarizer.py::TestClaudeSummarizer::test_summarize_success
```

### Example Usage

You can also run the example code in each module directly:

```bash
python html_extractor.py
python email_processor.py
python summarizer.py
python summary_writer.py
```

## Contributing

Whether you're a seasoned developer or just getting started, there are many ways to get involved:

### Ways to Contribute

- 🐛 **Report Bugs**: Found a bug? Let me know by creating an issue!
- 💡 **Suggest Features**: Have an idea for a new feature? I'd love to hear it!
- 📝 **Improve Documentation**: Help make docs clearer and more helpful
- 💻 **Write Code**: Pick up an issue or suggest your own improvements

### Getting Started

1. Check out our [open issues](https://github.com/Frodigo/garage/issues?q=is%3Aissue%20state%3Aopen%20label%3ANitroDigest) to see what needs help
2. Join our [discussions](https://github.com/Frodigo/garage/discussions) to share ideas
3. Fork the repo and create a new branch for your changes
4. Submit a pull request - we'll help you through the process!

### Development Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Write tests for new functionality
- Update documentation as needed
- Keep dependencies minimal and document why new ones are added

Don't worry if you're not sure about something - we're here to help! Just open an issue or start a discussion, and we'll guide you through the process.

## License

This project is open source under the MIT License.

## Acknowledgements

This project was inspired by NewslettersSummaryConsole.
