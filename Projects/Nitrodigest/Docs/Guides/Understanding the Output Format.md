---
permalink: projects/nitrodigest/docs/guides/understanding-the-output-format
---
---

Nitrodigest produces output in specific format. Take a look at the structure of generated summaries and see how to work with the results effectively.

## Standard Output Structure

Output includes both metadata and the actual summary content. Here's what a typical output looks like:

```yaml
---
date: '2025-09-19 19:25:20'
id: README.md
model: mistral
source: file:///home/frodigo/Work/garage/README.md
summary_date: '2025-09-29 07:51:03'
title: README.md
tokens: 262
---

# Summary

1. The text discusses a programming space, referred to as 'the garage', that values traditional programming and independence. It expresses concern over the role of programmers in the AI era being reduced to editors, arguing for the importance of 'vibe coding' and human creativity. The text also introduces a list of principles inspired by the Zen of Python. It provides details about the structure and content available on the site, including blog posts, projects, testimonials, and licensing information.
2. The text also mentions options for staying updated with the author's content such as RSS feed subscription, newsletter subscription, and following the author on GitHub. It emphasizes that all content is open-source and available online or in a GitHub repository.
3. Lastly, it provides instructions for contributing to the open-source projects through reporting bugs, suggesting ideas, and submitting pull requests.

# Tags

1. programming
2. traditional programming
3. AI
4. garage
5. Zen of Python
6. open source
7. contributing
```

## Output Format Components

### YAML Frontmatter

The output begins with YAML frontmatter containing metadata about the processing:

```yaml
---
title: document-name.txt
source: file:///absolute/path/to/document-name.txt
date: '2025-05-16 07:50:22'
id: document-name.txt
summary_date: '2025-05-26 07:55:46'
model: mistral
tokens: 189
---
```

**Field Descriptions:**

- **`title`**: The original filename or document title
- **`source`**: Full file path with `file://` protocol prefix
- **`date`**: Original file's last modification date and time
- **`id`**: Unique identifier (typically the file path)
- **`summary_date`**: When the summary was generated
- **`model`**: AI model used for summarization (e.g., mistral, llama2)
- **`tokens`**: Number of tokens processed by the model

### Summary Content

After the YAML frontmatter, the actual summary content follows. The format depends on your prompt template:

**Default Format (Numbered lists):**

```bash
1. Key point 1 with relevant details and context
2. Key point 2 highlighting important information
3. Key point 3 including any action items or deadlines
```

### Tags

Nitrodigest extracts tags from text and return them as list. Thanks to tags you can see what topics are described in the provided text:

```bash
# Tags

1. programming
2. traditional programming
3. AI
4. garage
5. Zen of Python
6. open source
7. contributing
```

## Directory Processing

When processing multiple files, each file gets its own complete output block:

```bash
nitrodigest documents/
```

**Output:**

```yaml
---
title: meeting-notes.txt
source: file:///home/user/documents/meeting-notes.txt
date: '2025-05-15 09:15:30'
id: documents/meeting-notes.txt
summary_date: '2025-05-29 14:25:10'
model: mistral
tokens: 142
---

<text 1 summary content>

---
title: project-report.md
source: file:///home/user/documents/project-report.md
date: '2025-05-20 16:45:22'
id: documents/project-report.md
summary_date: '2025-05-29 14:25:45'
model: mistral
tokens: 287
---

<text 2 summary content>
```

## Working with Output

### Saving Output to Files

**Single Summary:**

```bash
nitrodigest document.txt > summary.md
```

**Multiple Summaries:**

```bash
nitrodigest documents/ > all-summaries.md
```

**Appending to Existing File:**

```bash
nitrodigest new-document.txt >> existing-summaries.md
```

## Custom Output Formats

### Using Custom Prompt Templates

You can control the summary content format through prompt templates:

**Structured Output Template:**

```bash
Summarize this document using the following structure:

**Overview:** One sentence describing the main topic
**Key Points:**
- Point 1
- Point 2
- Point 3
**Action Items:** Tasks or next steps if any
```

**Table Format Template:**

```bash
Create a summary table for this document:

| Category | Details |
|----------|---------|
| Main Topic | Brief description |
| Key Findings | Most important discoveries |
| Recommendations | Suggested actions |
| Timeline | Important dates or deadlines |
```

### Including Original Text

By default, NitroDigest only outputs the summary. You can include the original text alongside the summary using the `--include-original` flag:

```bash
# Include original text with summary
nitrodigest document.txt --include-original
```

**Text Format Output with Original:**

```yaml
---
title: document-name.txt
source: file:///absolute/path/to/document-name.txt
date: '2025-05-16 07:50:22'
id: document-name.txt
summary_date: '2025-05-26 07:55:46'
model: mistral
tokens: 189
---

# Summary

1. Key summary points here...
2. Additional summary content...

# Tags

1. tag1
2. tag2

---

## Original Text

[The complete original text content would appear here]
```

**JSON Format with Original:**

```json
{
  "summary": ["Summary content here..."],
  "tags": ["tag1", "tag2"],
  "metadata": {
    "title": "document.txt",
    "source": "file:///path/to/document.txt",
    "date": "2025-05-16 07:50:22",
    "id": "document.txt"
  },
  "original_text": "The complete original text content would appear here"
}
```

### JSON Structured Output

You can use the `--format` flag to change output format to JSON:

```bash
$ nitrodigest README.md --format json

{
  "summary": [
    "The text discusses a programming space that values traditional coding, expressing concern over the increasing reliance on AI in modern programming, which they believe is reducing the creativity and problem-solving skills of programmers. The authors argue for maintaining a balance between AI and traditional coding.",
    "The text provides information about what can be found on the author's GitHub repository, including README, About, Now, Contact, Blog, Projects, Testimonials, Privacy policy, AI usage, Contributing, and Licensing files. It also mentions an RSS newsletter for staying updated.",
    "The text concludes by stating that all content on the GitHub repository is open-source and provides details about how to contribute."
  ],
  "tags": [
    "programming",
    "AI",
    "traditional coding",
    "garage",
    "balance",
    "open-source"
  ],
  "metadata": {
    "title": "README.md",
    "source": "file:///home/frodigo/Work/garage/README.md",
    "date": "2025-09-19 19:25:20",
    "id": "README.md"
  }
}
```

### Default JSON schema

At the moment JSON schema used by NiutroDigest is hardcoded and looks like this:

```json
 "format": {
	"type": "object",
	"properties": {
		"summary": {
			"title": "Summary",
			"description": "Summarize content into simple and short sentences",
			"type": "array",
			"items": {
				"type": "string"
			}
		},
		"tags": {
			"title": "Tags",
			"description": "Extract specific technical tags: programming languages, frameworks, design patterns, algorithms, and domain areas. Prioritize concrete technologies over abstract concepts.",
			"type": "array",
			"items": {
				"type": "string"
			}
		}
	},
	"required": [
		"summary",
		"tags"
	]
}

```

## Next Steps

- **[Summarizing email newsletter](../Use%20Cases/Summarizing%20Email%20Newsletters.md):** Learn how to summarize newsletters

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
