# Garage

A place for engineers who value traditional programming over vibe coding.

## Why this exists

Modern programming in the AI ​​era **relegates the programmer to the role of an editor**. Corporations force us to use AI for everything and tell us that it will be faster and better, but **is faster always better?**

Besides, vibe coding makes us as programmers lazy and stops us from thinking. We become useless. This is not how we imagined our work when we wrote our first "Hello World!" in Turbo Pascal many years ago.

Corporations with their challenges promise that AI will replace entire teams of programmers. Maybe someday it will, but should we allow it? **Should we give up without a fight?**

Where are the leaders? Well, they write books about Vibe coding.

This garage exists as a space for people who want to **solve problems with code**. We also use AI here because we like new technologies. But **we use AI; AI doesn't use us**.

Even when our world crumbles and we're forced into vibe coding at corporate jobs, we can always come back to the garage and code the way we love—simply for the joy of programming itself.

**Eviva l'arte!**

## What you can find here

### Nitrodigest

CLI tool that allows to TLDR text privately using local LLM models.

Currently in alpha version, under development. Contributors welcome!

### Testtrack

Experiments

### Website

The content of [https://frodigo.com](https://frodigo.com) website

## Licensing

This repository uses a dual licensing model:

### Code license

All code in this repository is licensed under the MIT License. This includes all source files, scripts, and configuration files. See [LICENSE-CODE](LICENSE-CODE) for details.

### Content License

All website content including blog posts, articles, documentation, images, and other media files in the `/website` directory is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

This means you are free to:

- Share — copy and redistribute the content in any medium or format
- Adapt — remix, transform, and build upon the content

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the content for commercial purposes.

For more details, see [LICENSE-WEBSITE](./website/LICENSE-WEBSITE)

## Contributing

Here's how you can help:

- **Report bugs** by opening an issue
- **Suggest features** or ideas
- **Submit pull requests** for bug fixes or new features
- **Ask questions** if something isn't clear
- **Start discussion** to talk with real people instead of AI bots

### Precommit setup

This project uses pre-commit hooks. Follow instructions below to enable precommit hook
for this repository on your local machine

#### Installation

1. Install pre-commit if you don't have it:

```bash
pip install pre-commit
```

2. Install the git hook scripts:

```bash
pre-commit install
```

#### Configuration

The project has the following pre-commit hooks configured:

- **pre-commit-hooks**:

  - `trailing-whitespace`: Removes trailing whitespace
  - `end-of-file-fixer`: Ensures files end with a newline

- **autopep8**:

  - Automatically formats Python code according to PEP 8

- **markdownlint-cli2**:
  - Lints and automatically fixes Markdown files

### Usage

Once installed, the pre-commit hooks will run automatically on every commit.

To manually run all pre-commit hooks on all files:

```bash
pre-commit run --all-files
```

To run a specific hook:

```bash
pre-commit run <hook-id> --all-files
```

For example, to run only markdownlint:

```bash
pre-commit run markdownlint-cli2 --all-files
```
