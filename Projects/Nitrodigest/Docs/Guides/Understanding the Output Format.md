---
permalink: projects/nitrodigest/docs/guides/understanding-the-output-format
---
---

Nitrodigest produces output in specific format. Take a look at the structure of generated summaries and see how to work with the results effectively.

## Standard Output Structure

Output includes both metadata and the actual summary content. Here's what a typical output looks like:

```yaml
---
title: example.txt
source: file:///home/user/documents/example.txt
date: '2025-05-16 07:50:22'
id: example.txt
summary_date: '2025-05-26 07:55:46'
model: mistral
tokens: 189
---

- Project kickoff meeting scheduled for June 3rd with stakeholders from engineering and design teams
- New authentication system implementation 70% complete, requiring final testing phase next week
- Database performance optimization needed to reduce query response time from 3 seconds to under 1 second
- Updated design system documentation deadline set for Wednesday, including new accessibility compliance features
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

**Default Format (Bullet Points):**

```bash
- Key point 1 with relevant details and context
- Key point 2 highlighting important information
- Key point 3 including any action items or deadlines
```

## Output Variations by Content Type

### Single File Processing

```bash
nitrodigest --input document.txt
```

**Output:**

```yaml
---
title: document.txt
source: file:///home/user/document.txt
date: '2025-05-16 08:30:15'
id: document.txt
summary_date: '2025-05-29 14:22:33'
model: mistral
tokens: 156
---

- Document contains quarterly sales report showing 23% increase in revenue
- Key performance indicators exceeded targets in Q2 with customer satisfaction at 4.8/5
- Recommendations include expanding sales team and investing in customer support tools
```

### Directory Processing

When processing multiple files, each file gets its own complete output block:

```bash
nitrodigest --input documents/
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

- Team meeting covered sprint planning and resource allocation for Q3 projects
- Decision made to prioritize authentication feature over reporting dashboard
- Next meeting scheduled for June 5th to review progress and address blockers

---
title: project-report.md
source: file:///home/user/documents/project-report.md
date: '2025-05-20 16:45:22'
id: documents/project-report.md
summary_date: '2025-05-29 14:25:45'
model: mistral
tokens: 287
---

- Project status shows 75% completion with June 15th target deadline on track
- Technical challenges resolved in authentication system, testing phase begins next week
- Budget utilization at 85% with remaining funds allocated for final testing and deployment
```

## Working with Output

### Saving Output to Files

**Single Summary:**

```bash
nitrodigest --input document.txt > summary.md
```

**Multiple Summaries:**

```bash
nitrodigest --input documents/ > all-summaries.md
```

**Appending to Existing File:**

```bash
nitrodigest --input new-document.txt >> existing-summaries.md
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

### JSON-like Structured Output

**Custom Prompt for JSON-style Output:**

```bash
Summarize this document in the following structured format:

TOPIC: [Main subject]
PRIORITY: [High/Medium/Low]
SUMMARY: [2-3 sentence overview]
DETAILS: [Key points as numbered list]
ACTIONS: [Required actions if any]
DEADLINE: [Important dates]
```

### Formatting Problems

**Inconsistent bullet points or structure:**

- Use custom prompt templates for better control
- Consider two-pass processing for format refinement

## Next Steps

- **[Summarizing email newsletter](../Use%20Cases/Summarizing%20Email%20Newsletters.md):** Learn how to summarize newsletters

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
