---
permalink: projects/nitrodigest/docs/getting-started/quickstart
---
Once you have NitroDigest installed, here’s a quick example to verify everything is working:

## 1. Prepare a test file

Create a simple text file `example.txt` with some content (for instance, you can copy a few paragraphs from a news article or an email newsletter).

## 2. Run NitroDigest on the file

```bash
nitrodigest example.txt
```

This command will use the default settings to summarize `example.txt`. The tool will connect to the local Ollama model, generate a summary, and save the result.

## 3. Observe the output

You should see console messages indicating the file is being processed and where the summary is saved. For example:

```bash
Processing file: example.txt
Generating summary for example.txt...
2025-05-16 08:11:51,550 - cli.summarizer.base.OllamaSummarizer - INFO - Sending request to Ollama API using model mistral
```

When the process is done, you will see a summary in terminal.

If you want to save the summary into a file, please use command like this:

```bash
nitrodigest example.txt > summary.md
```

When the process is done, you can simply see the summary from file. Example:

```bash
cat summary.md
```

## 4. Including Original Text (Optional)

If you want to include the original text alongside the summary, use the `--include-original` flag:

```bash
nitrodigest example.txt --include-original > summary-with-original.md
```

This will append the original text to the output after the summary, which can be useful for reference or comparison purposes.

Read next:

- [Summarizing All Files in a Directory](Summarizing%20All%20Files%20in%20a%20Directory.md)
- [Overriding Prompt Templates](Overriding%20Prompt%20Templates.md)
- [Understanding the Output Format](Understanding%20the%20Output%20Format.md)
- [Using a Custom Configuration](Using%20a%20Custom%20Configuration.md)

---
Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs
