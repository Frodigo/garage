---
permalink: projects/nitrodigest/docs/guides/overriding-prompt-templates
---
---

This guide explains how to customize NitroDigest's summarization behavior by creating and using custom prompt templates. Custom prompts allow you to customize summaries for specific content types, focus areas, or output formats.

## Understanding Prompt Templates

NitroDigest uses prompt templates to instruct the AI model on how to summarize your content. The default template works well for general documents, but custom prompts can significantly improve results for specialized content like:

- Technical documentation
- Meeting notes requiring action items
- Research papers needing key findings
- Financial reports focusing on metrics
- Code documentation emphasizing implementation details

## Methods for Overriding Prompts

NitroDigest offers three ways to customize prompts, in order of priority:

1. **Direct prompt content** (highest priority)
2. **Prompt template file** (medium priority)
3. **Configuration file** (lowest priority)

## Method 1: Direct Prompt Content

Use the `--prompt` argument to provide prompt content directly in the command line:

```bash
=nitrodigest --input document.txt --prompt "Summarize this document focusing on action items and deadlines. Format the output as a bulleted list."=
```

### Advantages

- Quick and convenient for one-off customizations
- No need to create separate files
- Perfect for testing different prompt approaches

### Disadvantages

- Not reusable across sessions
- Command line can become unwieldy with long prompts
- Shell escaping issues with quotes and special characters

### Example: Meeting Notes Focus

```bash
nitrodigest --input meeting.txt --prompt "Extract and summarize the key decisions, action items, and deadlines from this meeting. Format as: DECISIONS: ..., ACTION ITEMS: ..., DEADLINES: ..."
```

### Example: Technical Documentation

```bash
nitrodigest --input api-docs.md --prompt "Summarize this technical documentation highlighting: 1) Main purpose/functionality, 2) Key parameters and methods, 3) Usage examples, 4) Important limitations or considerations."
```

## Method 2: Prompt Template Files

For reusable prompts, create template files and reference them with `--prompt-file`:

```bash
nitrodigest --input document.txt --prompt-file custom-prompt.txt
```

### Creating Prompt Template Files

Create a plain text file containing your prompt template:

**prompt_technical_summary.txt:**

```bash
Analyze this technical document and provide a structured summary with the following sections:

## Overview
Briefly describe what this document covers and its main purpose.

## Key Technical Points
List the most important technical details, specifications, or requirements.

## Implementation Notes
Highlight any important implementation details, dependencies, or considerations.

## Action Items
If present, extract any tasks, recommendations, or next steps.

Keep the summary concise but comprehensive, focusing on information that would be valuable for technical team members.
```

**prompt_meeting_notes.txt:**

```bash
Please summarize this meeting content with the following structure:

**Meeting Summary:**
- Brief overview of the meeting purpose and main topics

**Key Decisions:**
- List important decisions made during the meeting

**Action Items:**
- Extract specific tasks assigned to individuals with deadlines if mentioned

**Follow-up Required:**
- Note any items requiring future discussion or clarification

Format the output clearly and focus on actionable information.
```

**prompt_research_paper.txt:**

```bash
Summarize this research document focusing on:

1. **Research Question/Hypothesis**: What problem is being addressed?
2. **Methodology**: How was the research conducted?
3. **Key Findings**: What are the main results or discoveries?
4. **Implications**: What do these findings mean for the field?
5. **Limitations**: What are the acknowledged limitations or areas for future research?

Keep the summary academic but accessible, suitable for someone familiar with the general field but not necessarily the specific research area.
```

### Using Template Files

```bash
# Use technical summary template
nitrodigest --input api-documentation.md --prompt-file prompt_technical_summary.txt

# Use meeting notes template
nitrodigest --input team-meeting.txt --prompt-file prompt_meeting_notes.txt

# Use research template
nitrodigest --input research-paper.pdf --prompt-file prompt_research_paper.txt
```

### Template File Best Practices

**Clear Instructions:** Be specific about what you want the AI to focus on and how to structure the output.

**Structure Guidelines:** Provide clear formatting instructions (headings, bullet points, sections).

**Context Setting:** Explain the intended audience or use case for the summary.

**Length Guidance:** Specify if you want brief overviews or detailed summaries.

## Advanced Prompt Techniques

### Multi-prompting

One powerful technique is to run Nitrodigest two times on the same set of data. This is useful, for example, when you want to ensure that the formatting of the result is correct. LLMs sometimes return summaries in formats that don't match your intended structure.

#### First Pass - Extract Content

```bash
nitrodigest --input document.pdf --prompt "Summarize the key points, findings, and important information from this document. Focus on capturing all essential content. Return a bullet lists" > raw-summary.md
```

#### Second Pass - Format Refinement

```bash
nitrodigest --input raw-summary.md --prompt "Forrmat this summary into a bullet list that have heading + paragraph" > final-summary.md
```

#### Single Command

You can chain both passes in one command using shell piping:

```bash
nitrodigest --input document.pdf --prompt "Summarize key points and findings" | nitrodigest --input /dev/stdin --prompt "Reformat this content with clear headings, bullet points, and professional structure" > formatted-summary.md
```

### Directory Processing with Custom Prompts

Apply the same custom prompt to all files in a directory:

```bash
# Summarize all meeting notes with consistent format
nitrodigest --input meeting-notes-folder/ --prompt-file meeting-template.txt > all-meetings-summary.md
```

### Prompt Optimization Tips

**Be Specific:** Instead of "summarize this," specify what aspects to focus on.

**Use Examples:** Show the AI what good output looks like:

```bash
Format your response like this example:
SUMMARY: Brief overview in 2-3 sentences
ACTIONS: - Action item 1, - Action item 2
DEADLINE: Next Friday
```

**Set Expectations:** Specify length, tone, and audience:

```bash
Create a 200-word executive summary suitable for non-technical stakeholders...
```

**Test Iteratively:** Start with simple prompts and refine based on results.

## Next Steps

- **[Output Formats](./Understanding%20the%20Output%20Format.md):** Learn about Understanding the Output Format
- **[Configuration](Using%20a%20Custom%20Configuration.md):** Explore Using a Custom Configuration for managing defaults

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
