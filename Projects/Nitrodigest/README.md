# NitroDigest

TL;DR your data, privately.

**NitroDigest – the privacy‑first, local‑LLM text‑summariser for developers.**

This project is in alpha phase.

## Features

- Runs 100 % on‑device with Ollama – your private data never leaves localhost
- Command-line interface with various options
- Completely free (open source, MIT license)

---

## Usage

### Prerequisites

To run this tool, you needs to have [Ollama](https://ollama.com/download) and [Python](https://www.python.org/downloads/) installed on your local machine.

### Installation

`pip install nitrodigest-cli`

### Basic Usage

Run NitroDigest with the default configuration:

```bash
nitrodigest <file or directory you want to summarize> > <destination where to want to save summary>
```

#### Examples

**Process current directory** (summarize all files in the current working directory):

```bash
nitrodigest > summary.md
```

Summarize one file and save it to summary.md:

```bash
nitrodigest my_long_text.html > summary.md
```

Summarize files in a directory and save them in a summary.md:

```bash
nitrodigest my_directory/ > summary.md
```

### Command Line Arguments

You can override any configuration setting using command line arguments:

```bash
nitrodigest \
    --model mistral \
    --timeout 800
```

Available arguments:

- `--timeout`: Time in seconds for API requests to Ollama (default: 300)
- `--prompt-file`: Path to custom prompt template file (overrides default one)
- `--prompt`: Direct prompt content (overrides prompt-file)
- `--model`: Model that will be used for summarization (default: mistral)
- `--ollama_api_url`: URL of Ollama API (default: <http://localhost:11434>)
- `--format`: Output format. Can be `text` or `json` (default: text)
- `--include-original`: Include original text in the summary output (default: False)

### Custom Prompt Configuration

You can specify a custom prompt in two ways

1. Using the `--prompt-file` argument:

```bash
nitrodigest --prompt-file custom_prompt.txt
```

2. Passing the prompt content directly:

```bash
nitrodigest --prompt "$(cat my_awesome_prompt.txt)"
```

The prompt template should contain placeholders:

- `{metadata}`: it's used to render information like source, title, and date
- `{text}`: For the text content to be summarized

---

## Contributing

Do you want to contribute this tool? Check the Contributing page:

[Getting started](Getting%20started.md)

## Report an issue

Found an issue? You can easily report it here:

[https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
