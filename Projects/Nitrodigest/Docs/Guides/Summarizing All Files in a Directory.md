---
permalink: projects/nitrodigest/docs/guides/summarizing-all-files-in-a-directory
---
This guide shows you how to process multiple files at once by pointing NitroDigest at a directory. This is perfect when you have a folder full of documents, articles, or notes that you want to summarize in batch.

## Basic Directory Processing

The simplest way to process all supported files in a directory is:

```bash
nitrodigest /path/to/directory
```

This command will:

1. Scan the directory and all subdirectories
2. Find all supported text files
3. Process each file individually using your default model
4. Output each summary to the terminal in sequence

### Process Current Directory

You can also run NitroDigest without any arguments to automatically process all supported files in your current working directory:

```bash
nitrodigest
```

This is particularly useful when you're already in the directory you want to process and don't want to specify the path explicitly.

## Supported File Types

NitroDigest automatically processes files with these extensions:

- **Text files:** `.txt`, `.log`
- **Markdown files:** `.md`, `.markdown`
- **Web content:** `.html`, `.htm`
- **Structured data:** `.xml`, `.json`, `.csv`

Files with other extensions are skipped automatically.

## Basic Example

Let's say you have a directory structure like this:

```bash
documents/
├── meeting-notes.txt
├── project-report.md
├── data-analysis.csv
├── webpage.html
├── image.jpg          # Will be skipped
└── subdirectory/
    └── more-notes.txt
```

Running:

```bash
nitrodigest documents/
```

Will process `meeting-notes.txt`, `project-report.md`, `data-analysis.csv`, `webpage.html`, and `subdirectory/more-notes.txt`. The `image.jpg` file will be skipped since it's not a supported text format.

## Output Options

### Terminal Output (Default)

By default, all summaries are displayed in your terminal one after another:

```bash
nitrodigest documents/
```

You'll see processing messages and formatted summaries for each file:

```bash
Processing directory: documents/
Processing file: documents/meeting-notes.txt
Generating summary for meeting-notes.txt...
2025-05-26 07:55:42,615 - cli.summarizer.base.OllamaSummarizer - INFO - Sending request to Ollama API using model mistral
---
date: '2025-05-16 07:50:22'
id: documents/meeting-notes.txt
model: mistral
source: file:///home/user/documents/meeting-notes.txt
summary_date: '2025-05-26 07:55:46'
title: meeting-notes.txt
tokens: 189
---

<summary of meeting-notes.txt>

Processing file: documents/project-report.md
Generating summary for project-report.md...
...
Directory processing complete: 4 of 4 files processed successfully
```

### Save All Summaries to One File

To collect all summaries in a single file:

```bash
nitrodigest documents/ > all_summaries.md
```

This creates a comprehensive document with all summaries combined, making it easy to review everything at once.

### Append to Existing File

To add directory summaries to an existing summary collection:

```bash
nitrodigest new_documents/ >> existing_summaries.md
```

## Working with Different Directory Sizes

### Small Directories

For directories with just a few files, processing is straightforward and fast:

```bash
nitrodigest my_notes/
```

Or if you're already in the directory:

```bash
cd my_notes/
nitrodigest
```

## Directory Processing Behavior

### Recursive Processing

NitroDigest processes directories recursively, meaning it will find and process files in subdirectories automatically:

```bash
project/
├── main_docs/
│   ├── overview.md
│   └── technical/
│       └── specifications.txt
└── notes.txt
```

All three files (`overview.md`, `specifications.txt`, and `notes.txt`) will be processed.

### File Ordering

Files are processed in the order they're discovered by the file system, which typically means:

- Files in the main directory first
- Then files in subdirectories

## Practical Use Cases

### Research Document Collection

Process a folder of research papers or articles:

```bash
nitrodigest research_papers/ > research_summary.md
```

### Project Documentation

Summarize all documentation in a project:

```bash
nitrodigest project_docs/ > project_overview.md
```

### Email Archive

Process exported email files:

```bash
nitrodigest email_exports/ > email_summaries.md
```

### Meeting Notes Collection

Summarize a month's worth of meeting notes:

```bash
nitrodigest meeting_notes_march/ > march_meetings_summary.md
```

## Tips and Best Practices

### Organize Your Input

Structure your directories logically before processing:

```bash
# Good organization
documents/
├── 2025-may/
├── 2025-april/
└── archive/
```

### Filter by Date

If you want to process only recent files, consider organizing them by date first, then process specific subdirectories:

```bash
nitrodigest documents/2025-may/
```

### Preview Before Processing

For large directories, you might want to see what files will be processed first:

```bash
find documents/ -name "*.txt" -o -name "*.md" -o -name "*.html" -o -name "*.htm" -o -name "*.xml" -o -name "*.json" -o -name "*.csv" -o -name "*.log"
```

### Backup Important Directories

Before processing important document collections, consider backing them up, especially if you plan to append summaries to the original files.

## Troubleshooting

### No Files Found

```bash
Processing directory: empty_folder/
Directory processing complete: 0 of 0 files processed successfully
```

**Solution:** Check that the directory contains supported file types and that you have read permissions.

## Advanced Usage

### Custom Models for Directory Processing

Use a different model for the entire directory:

```bash
nitrodigest documents/ --model llama2 > llama2_summaries.md
```

### Custom Prompts for Specialized Content

If your directory contains specialized content, use a custom prompt:

```bash
nitrodigest technical_docs/ --prompt "Summarize this technical document focusing on implementation details and requirements" > tech_summaries.md
```

## Next Steps

- **[Custom Prompts](./Overriding%20Prompt%20Templates.md):** Explore Overriding Prompt Templates for specialized content
- **[Output Formats](Understanding%20the%20Output%20Format.md):** Read about Understanding the Output Format
- **[Configuration](./Using%20a%20Custom%20Configuration.md):** Check out Using a Custom Configuration for advanced setups

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
