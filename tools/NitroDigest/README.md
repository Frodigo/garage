# NitroDigest

A Python tool for automatically summarizing email newsletters using AI.

## Features

- Connect to IMAP email servers to retrieve unread newsletters
- Extract text content from HTML emails
- Two-step summarization process:
  1. Initial summary with key points and links
  2. Refined summary with single-sentence bullets and links (Note: in the current implementation this step is disabled)
- Summarize content using various AI models:
  - Claude (Anthropic)
  - ChatGPT (OpenAI)
  - Ollama (local models)
- Save all summaries in a single combined Markdown file with YAML frontmatter
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

#### Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

#### Using conda

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

Rename `config.json.sample` file to `config.json` and fill it with your own values.

Config structure:

```json
{
  "email": {
    "address": "your-email@gmail.com",
    "password": "your-password-or-app-password",
    "server": "imap.gmail.com",
    "port": 993,
    "folder": "INBOX"
  },
  "summarizer": {
    "type": "ollama",
    "model": "nitroModel",
    "base_url": "http://localhost:11434",
    "timeout": 300
  },
  "summaries_path": "summaries",
  "limit": 5,
  "mark_as_read": true
}
```

### Configuration Options

#### Email Settings

- `email.address`: Your email address
- `email.password`: Your email password or app password
- `email.server`: IMAP server (default: "imap.gmail.com")
- `email.port`: IMAP port (default: 993)
- `email.folder`: Email folder to process (default: "INBOX")

#### Summarizer Settings

- `summarizer.type`: One of "claude", "chatgpt", or "ollama"
- `summarizer.model`: Model name to use (for Ollama)
- `summarizer.base_url`: Base URL for Ollama (default: [http://localhost:11434])
- `summarizer.api_key`: API key for Claude or ChatGPT (required for those services)
- `summarizer.timeout`: time in seconds that summarizer waits for response from LLM

#### General Settings

- `summaries_path`: Directory to save summaries (default: "summaries")
- `limit`: Maximum number of emails to process (default: 5)
- `mark_as_read`: Whether to mark processed emails as read (default: true)

### Gmail Configuration

If you're using Gmail, you'll need to:

1. Enable IMAP in your Gmail settings. For personal accounts it is enabled already, and this option is not visible in settings.
2. Create an app password if you have 2-factor authentication enabled, or if your regular password is not working, and you get authentication errors when attempting to use NitroDigest.
   - Go to [app passwords settings](https://myaccount.google.com/apppasswords).
   - Add new "app" with whatever name you want, then generate the 16-character password. This password can now be used instead of your regular password.

## Ollama docker setup

Follow this guide if you want to run Ollama on your local machine.

### Prerequisites

- Docker and Docker Compose installed on your system
- Sufficient disk space (at least 10GB recommended, ideally 20% of your total disk space)
- For optimal performance: At least 8GB of RAM
- Optional for enhanced performance: NVIDIA GPU with proper drivers (for GPU acceleration)

### Run Ollama on docker using predefined docker compose

In the `ollama` directory you can find a `docker-compose.ollama.yml` file which contains setup
for `Olama` and `Open WebUI`.

1. To start Ollama run:

```bash
cd ollama
docker-compose -f docker-compose.ollama.yml up
```

Note that first build could take some time (~10-20min - depending on the internet connection)

1. Access the Ollama API directly at [http://localhost:11434](http://localhost:11434) or the web interface at [http://localhost:3000](http://localhost:11434)

Note: make sure that you have correct configuration in your `config.json` or `.env` file.

### Installing new models

If you want to install new models you have three options.

1. Update the Modelfile
2. Using the command line
3. Using the Web UI

#### Updating the Modelfile

1. Modify ollama/Modelfile and change model there.
2. Rebuild the container`

#### Using the command line

1. Access the Ollama container:

```bash
docker exec -it ollama /bin/bash
```

1. Pull a model:

```bash
ollama pull llama2
```

Replace "llama2" with any model you want to use (e.g., deepseek-r1, llava-phi3)

1. Run the model:

```bash
ollama run llama2
```

#### Using the Web UI

1. Navigate to [http://localhost:3000](http://localhost:3000) in your browser.
2. Create an account if prompted.
3. Go to the Models section and select "Pull a model from Ollama.com"
4. Choose from available models like llama2, deepseek-coder, etc.

## Usage

### Basic Usage

Run NitroDigest with the default configuration file (`config.json`):

```bash
python main.py
```

### Using a Custom Configuration File

If you want to use a different configuration file:

```bash
python main.py --config custom_config.json
```

### Command Line Arguments

You can override any configuration setting using command line arguments:

```bash
python main.py \
    --limit 10 \
    --output-dir custom_summaries \
    --summarizer ollama \
    --model mistral \
    --mark-as-read \
    --email custom@example.com \
    --password custom-password \
    --server imap.example.com \
    --folder CUSTOM_FOLDER
```

Available arguments:

- `--config`: Path to configuration file (default: config.json)
- `--limit`: Maximum number of emails to process
- `--output-dir`: Directory to save summaries
- `--mark-as-read`: Mark processed emails as read
- `--email`: Email address (overrides config)
- `--password`: Email password (overrides config)
- `--server`: IMAP server (overrides config)
- `--folder`: Email folder to process
- `--timeout`: Time in seconds that summarizer waits for response from LLM
- `--prompt-file`: Path to custom prompt template file (overrides config)
- `--prompt`: Direct prompt content (overrides both config and prompt-file)

### Prompt Configuration

You can specify the prompt template in three ways:

1. In the config.json file:

```json
{
  "summarizer": {
    "prompt_file": "prompt_template.txt"
  }
}
```

2. Using the `--prompt-file` argument:

```bash
python main.py --prompt-file custom_prompt.txt
```

3. Passing the prompt content directly:

```bash
python main.py --prompt "$(cat my_awesome_prompt.txt)"
```

The prompt template should contain placeholders:

- `{metadata}`: For email metadata (from, subject, date)
- `{text}`: For the email content to be summarized

## Testing

Run tests using pytest:

```bash
pytest
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

This project is licensed under the MIT License - see the LICENSE file for details.

## Output Format

Summaries are saved in a single `combined_summaries.md` file in your specified output directory. Each summary includes:

- YAML frontmatter with metadata (title, source, date, etc.)
- The refined summary with single-sentence bullets and links
- Separators between different summaries

Example output structure:

```markdown
# Combined Newsletter Summaries

---

title: Tech Weekly Newsletter
source: tech@example.com
date: 2024-03-20
email_id: 12345
summary_date: 2024-03-20 14:30:00

---

- OpenAI released GPT-5 with improved reasoning [link]
- Apple announced M3 Pro chips with better performance [link]

---

// ... next summary ...
```
