---
permalink: projects/nitrodigest/docs
---
## Introduction

**NitroDigest** is a cross-platform command-line tool that **summarizes text files** – such as newsletters, emails, logs, notifications, markdown documents – into **TL;DR** form. It's distributed as Python package and runs on **Linux, macOS, and Windows.** It uses local Large Language Models via **Ollama** for processing. This means you can get TL;DR summaries **privately and offline**, without sending data to any cloud. NitroDigest can handle single files or batches of files, automatically chunking large texts to fit model token limits. It outputs summaries in a structured Markdown format that includes metadata, making it easy to read or integrate into other systems.

**Key Features:**

- **Local AI Summarization:** Uses Ollama to run LLMs on your machine, preserving privacy and working offline.
- **Multiple Input Formats:** Supports plain text, Markdown, HTML, CSV, JSON, and other text-based files.
- **Batch Processing:** Summarize a single file or all files in a directory in one command.
- **Configurable Prompts:** Uses prompt templates that you can customize to change the style or content of summaries.
- **Extensible:** Easily switch to different models (e.g., use a larger or domain-specific Ollama model) and adjust token budgets or segmentation for large inputs.

NitroDigest is a tool for developers. Goal of this documentation is to show how to install and use the tool. Use the sidebar or the table of contents below to navigate to different sections.

Note: this documentation is under development just like the tool. Not all sections are finished.

## Table of Contents

- **Getting Started**
    - [Installation](Installation.md)
    - [Quickstart](Quickstart.md)
- **Guides**
    - [Summarizing a Single File](Summarizing%20a%20Single%20File.md)
    - [Summarizing All Files in a Directory](Summarizing%20All%20Files%20in%20a%20Directory.md)
    - [Overriding Prompt Templates](Overriding%20Prompt%20Templates.md)
    - [Using a Custom Configuration](Using%20a%20Custom%20Configuration.md)
    - [Understanding the Output Format](Understanding%20the%20Output%20Format.md)
- **Use Cases**
    - [Summarizing Email Newsletters](Summarizing%20Email%20Newsletters.md)
    - [Summarizing Slack Messages](Summarizing%20Slack%20Messages.md)
    - [Summarizing GitHub Pull Requests](Summarizing%20GitHub%20Pull%20Requests.md)
- **Customization**
    - [Custom Prompt Templates](Custom%20Prompt%20Templates.md)
    - [Switching Models (Ollama Integration)](Switching%20Models%20(Ollama%20Integration).md)
    - [Adjusting Token Budgets & Segmentation](Adjusting%20Token%20Budgets%20&%20Segmentation.md)
- **Contributing
	- [Getting started](Getting%20started.md)
	- [Ollama setup](Ollama%20setup.md)

---
Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs
