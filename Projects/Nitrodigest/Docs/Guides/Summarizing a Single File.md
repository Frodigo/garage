---
permalink: projects/nitrodigest/docs/guides/summarizing-a-single-file
---
This guide covers how to process individual files with NitroDigest in detail. While the [[Quickstart]] shows the basic workflow, this page explores different options, file types, and common scenarios you'll encounter when summarizing single files.

## Basic Command Structure

The fundamental command for processing a single file is:

```bash
nitrodigest --input <filename>
```

This command will:

1. Read and analyze the specified file
2. Connect to your local Ollama model (default: mistral)
3. Generate a summary using the default prompt template
4. Display the summary in your terminal

## Supported File Types

NitroDigest can process various text-based file formats:

### Plain Text Files

```bash
nitrodigest --input document.txt
nitrodigest --input notes.log
nitrodigest --input readme.rst
```

### Markdown Files

```bash
nitrodigest --input article.md
nitrodigest --input documentation.markdown
```

### Web Content

```bash
nitrodigest --input webpage.html
nitrodigest --input email.htm
```

### Structured Data

```bash
nitrodigest --input data.json
nitrodigest --input report.csv
```

**Note:** when you process files like HTML that can contain many HTML tags, please try to extract text from the HTML before you run NitroDigest. It will encrease quality of the summary and decrease processing time.

## Output Options

### Terminal Output (Default)

By default, NitroDigest displays the summary directly in your terminal:

```bash
nitrodigest --input newsletter.txt
```

You'll see processing messages followed by the formatted summary:

```bash
Processing file: example.txt
Generating summary for example.txt...
2025-05-26 07:55:42,615 - cli.summarizer.base.OllamaSummarizer - INFO - Sending request to Ollama API using model mistral
---
date: '2025-05-16 07:50:22'
id: example.txt
model: mistral
source: file:///home/frodigo/Documents/nitrodigest-use-cases/example.txt
summary_date: '2025-05-26 07:55:46'
title: example.txt
tokens: 189
---

1. Guide on renaming and moving notes in Obsidian, with redirection of old links to new ones ([URL](https://publish.obsidian.md/username/about))
    - To rename a note and redirect old links:
      - Add the "permalink" property to your note's Properties.
      - Rename the URL according to your preference.
    - To move a note and redirect old links:
      - Move the note to its new location within the vault.
      - Obsidian automatically updates internal links, but external links may still point to the old location.
    - To redirect readers from old notes to new ones:
      - Add an alias in the note you want to redirect to, using the full path to the old note.

```

### Save to File

To save the summary to a file instead of displaying it in the terminal:

```bash
nitrodigest --input example.txt > example_summary.md
```

You can then view the saved summary:

```bash
cat example_summary.md
```

### Append to Existing File

To add summaries to an existing file:

```bash
nitrodigest --input example.txt >> all_summaries.md
```

A nice example for this approach is a case when you want to add a summary to the same file, that you summarize:

```bash
nitrodigest --input example2.txt >> example2.txt
```

## Working with Different File Sizes

### Small Files

For files under 1000 words, processing is typically fast and straightforward:

```bash
nitrodigest --input email.txt
```

### Large Files

NitroDigest automatically handles large files by chunking them to fit within model token limits. You'll see additional processing messages:

```bash
Generating summary for csv_docs.md...
2025-05-26 08:07:15,136 - cli.summarizer.base.OllamaSummarizer - INFO - Content exceeds token budget. Splitting into 7 chunks.
2025-05-26 08:07:15,136 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 1/7
2025-05-26 08:07:17,485 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 2/7
2025-05-26 08:07:18,584 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 3/7
2025-05-26 08:07:20,161 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 4/7
2025-05-26 08:07:22,477 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 5/7
2025-05-26 08:07:23,612 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 6/7
2025-05-26 08:07:25,063 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 7/7
2025-05-26 08:07:26,429 - cli.summarizer.base.OllamaSummarizer - INFO - Combined intermediate summaries are too long. Summarizing again.
2025-05-26 08:07:26,430 - cli.summarizer.base.OllamaSummarizer - INFO - Content exceeds token budget. Splitting into 2 chunks.
2025-05-26 08:07:26,430 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 1/2
2025-05-26 08:07:28,350 - cli.summarizer.base.OllamaSummarizer - INFO - Processing chunk 2/2

```

## Troubleshooting

### File Not Found

```bash
nitrodigest --input nonexistent.txt
# Error: Input path 'nonexistent.txt' does not exist
```

**Solution:** Check the file path and ensure the file exists in the current directory or provide the full path.

### Unsupported File Format

```bash
nitrodigest --input image.jpg
# Error processing file 'image.jpg': 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

```

**Solution:** NitroDigest works only with text-based files. Convert binary files to text format first if needed.

### Large File Processing

If processing very large files takes too long:

- Consider breaking the file into smaller sections
- Make sure that Ollama use GPU
- If your computer does not have enough processing power, consider deploying Ollama on a server with enough resources.

## Best Practices

**File Naming:** Use descriptive filenames to make your summaries more organized:

```bash
nitrodigest --input "2025-05-26_project_update.md" > "2025-05-26_project_summary.md"
```

**Batch Similar Files:** If you have multiple related files, consider using batch processing instead.

**Custom Prompts:** For specialized content, consider using custom prompt templates to get better results.

## Next Steps

- **[Process Multiple Files](./Summarizing%20All%20Files%20in%20a%20Directory.md):** Learn about Summarizing All Files in a Directory
- **[Customize Output](./Overriding%20Prompt%20Templates.md):** Explore Overriding Prompt Templates
- **[Understand Results](./Understanding%20the%20Output%20Format.md):** Read about Understanding the Output Format
- **[Advanced Configuration](./Using%20a%20Custom%20Configuration.md):** Check out Using a Custom Configuration

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
