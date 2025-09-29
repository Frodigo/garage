---
permalink: projects/nitrodigest/docs/guides/using-a-custom-configuration
---
---

In this guide I want to show you how to customize NitroDigest's default settings using configuration options. Custom configurations allow you to optimize performance, use different models, connect to remote Ollama instances, and set up default prompt templates for your workflow.

## Configuration Methods

NitroDigest supports configuration through command-line arguments. All settings have sensible defaults, so you only need to specify the options you want to change.

## Available Configuration Options

Let's explore what options you can configure.

### Model Selection

**Default:** `mistral`

Choose which AI model to use for summarization:

```bash
# Use the default Mistral model
nitrodigest document.txt

# Use Llama 2 model
nitrodigest document.txt --model llama2

# Use a specific model version
nitrodigest document.txt --model llama2:13b

# Use CodeLlama for technical documentation
nitrodigest code-docs.md --model codellama
```

**Available Models** depends on what you have installed in Ollama.

### Ollama API Configuration

**Default:** `http://localhost:11434`

Configure connection to your Ollama instance:

```bash
# Connect to Ollama on different port
nitrodigest  document.txt --ollama-api-url http://localhost:8080

# Connect to remote Ollama server
nitrodigest  document.txt --ollama-api-url http://your-server.com:11434

# Connect to Ollama with custom path
nitrodigest  document.txt --ollama-api-url http://localhost:11434/v1
```

### Timeout Configuration

**Default:** `300` seconds (5 minutes)

Adjust timeout for API requests to handle large documents or slower models:

```bash
# Short timeout for quick processing
nitrodigest  small-file.txt --timeout 60

# Extended timeout for large documents
nitrodigest  large-report.pdf --timeout 900

# Very long timeout for complex analysis
nitrodigest  massive-dataset.csv --timeout 1800
```

This configuration can be helpful when Ollama runs on CPU because in this case it's much slower than on GPU.

### Default Prompt Templates

Set a default prompt template that will be used unless overridden:

```bash
# Use custom prompt file as default
nitrodigest  document.txt --prompt-file my-template.txt

# Command-line arguments override prompt files
nitrodigest  document.txt --prompt-file my-template.txt --prompt "Quick summary only"
```

More about prompt configuration: [Overriding Prompt Templates](Overriding%20Prompt%20Templates.md)

### Output format

**Default:** `text`

Change output format to `json`:

```bash
nitrodigest  document.txt --format json
```

### Include Original Text

**Default:** `False`

Include the original text alongside the summary in the output:

```bash
# Include original text in summary output
nitrodigest document.txt --include-original

# Exclude original text (default behavior)
nitrodigest document.txt
```

When the `--include-original` flag is present, the original text will be appended after the summary in text format, or included as an `original_text` field in JSON format.

## Setting Up Default Configurations

### Environment Variables

At the moment NitroDigest doesn't directly support environment variables, you can use shell aliases for consistent configurations:

```bash
# Add to your .bashrc or .zshrc
alias nitro-fast="nitrodigest --model phi --timeout 120"

# Usage
nitro-fast quick-notes/
```

Then you can use this command just like this:

```bash
nitro-fast example.txt
```

### Configuration Scripts

You can create reusable configuration scripts for different use cases. Take a look at the example below.

**fast-processing.sh:**

```bash
#!/bin/bash
# Fast processing configuration
exec nitrodigest \
    --model phi \
    --timeout 120 \
    "$@"
```

Then, use your predefined script:

```bash
sh fast-processing.sh example.txt
```

## Next Steps

- **[Output Formats](Understanding%20the%20Output%20Format.md):** Explore Understanding the Output Format

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
