---
permalink: projects/nitrodigest/docs/contributting/getting-started
---

## How to contribute

- 🐛 **Report Bugs**: Found a bug? Create an issue!
- 💡 **Suggest Features**: Have an idea for a new feature? Start discussion!
- 💻 **Write Code**: Want to add/fix/change something? Create a PR!

In any case, feel free to start/join a discussion. I am interested in what you think about this tool.

### Getting Started

1. Check out [open issues](https://github.com/Frodigo/garage/issues?q=is%3Aissue%20state%3Aopen%20label%3ANitroDigest) to see what needs help
2. Join [discussions](https://github.com/Frodigo/garage/discussions) to share ideas (or create a new)
3. Fork the repo and create a new branch for your changes
4. Submit a pull request - we'll help you through the process!

### Development Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Keep dependencies minimal and document why new ones are added

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

```bash
# Clone the repository
git clone https://github.com/Frodigo/garage
cd Projects/Nitrodigest/src
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
pip install -r cli/requirements.txt
```

## Configuration

Rename `config.json.sample` file to `config.json` and fill it with your own values.

Config structure:

```json
{
    "model": "mistral",
    "ollama_api_url": "http://localhost:11434",
    "timeout": 300,
    "prompt_file": "prompt_template.txt",
}
```

### Configuration Options

- `model`: Model name to use
- `ollama_api_url`: Base URL for Ollama (default: [http://localhost:11434])
- `timeout`: time in seconds that summarizer waits for response from LLM
- `prompt_file`: path to prompt file

## Ollama docker setup

Follow this guide if you want to run Ollama on your local machine.
[Ollama setup](Ollama%20setup.md)

## Testing

Run tests using pytest:

```bash
pytest
```

### Test package on local

To build and test package on local use these commands from `garage/Projects/Nitrodigest` directory:

```bash
python -m build
pip install -e .
```

## Basic Usage

Run NitroDigest with the default configuration:

Make sure you are in the src directory and run command:

```bash
mkdir summaries
python run-nitrodigest-cli.py --input <file or directory you want to summarize> > summaries/summary.md
```
