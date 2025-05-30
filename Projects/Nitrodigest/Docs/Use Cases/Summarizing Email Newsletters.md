---
permalink: projects/nitrodigest/docs/use-cases/summarizing-email-newsletters
---
In this document I want to show you ho process and summarize email newsletters using NitroDigest in combination with **Himalaya**, a command-line email client.
## Prerequisites

Before starting, you'll need:

- **NitroDigest** installed and configured
- **Himalaya** email client installed ([https://github.com/pimalaya/himalaya](https://github.com/pimalaya/himalaya))
- Email account configured with Himalaya
- Ollama running locally with your preferred model

### Installing Himalaya

```bash
# Install via cargo (recommended)
cargo install himalaya

# Or download binary from releases
# https://github.com/pimalaya/himalaya/releases

# Configure your email account
himalaya account configure
```

## Basic Email Processing Workflow

### Step 1: List Unread Emails

Start by viewing your unread newsletters and emails:

```bash
himalaya envelope list not flag seen
```

**Example output:**

```bash
| ID   | FLAGS | SUBJECT                                           | FROM                    | DATE                    |
|------|-------|---------------------------------------------------|-------------------------|-------------------------|
| 1823 | *     | Google's IO conference was wild                   | Mindstream              | 2025-05-29 15:07+00:00 |
| 1822 | *     | Python Weekly - Issue 701                        | Python Weekly           | 2025-05-29 15:05+00:00 |
| 1821 | *     | Elon's xAI is paying Telegram $300M to adopt Grok| AI Valley               | 2025-05-29 14:54+00:00 |
| 1820 | *     | 🤖 Smartphone giant Honor enters humanoid race   | The Rundown Robotics    | 2025-05-29 14:32+00:00 |
| 1819 | *     | DeepSeek R1 Update 📚, Hugging Face CodeAgents 💻 | TLDR AI                 | 2025-05-29 13:26+00:00 |
```

### Step 2: Read Specific Email

Choose an email to process and save it to a file:

```bash
# Read email by ID and save to markdown file
himalaya message read 1823 > message.md
```

### Step 3: Generate Summary

Create a summary of the email content:

```bash
# Generate summary to separate file
nitrodigest --input message.md > message_summary.md

# Or append summary to the original email file
nitrodigest --input message.md >> message.md
```

---

Found an issue? Report a bug: [https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

#NitroDigest #Docs #NitroDigestDocs
