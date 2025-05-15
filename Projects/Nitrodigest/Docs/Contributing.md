## Contributing

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

## Testing

Run tests using pytest:

```bash
pytest
```

## Basic Usage

Run NitroDigest with the default configuration:

Make sure you are in the src directory and run command:

```bash
mkdir summaries
python run-nitrodigest-cli.py --input <file or directory you want to summarize> > summaries/summary.md
```
