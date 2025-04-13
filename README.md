# Garage

This is my monorepo where I store all my code and content. This is my *garage*.

At the moment here is the huge chaos because I am in process of importing here code from different sources.

## Repository structure

### Website

In the `website` directory you can find content of my website. You can also visit [https://frodigo.com](https://frodigo.com)

### Sandbox

I keep there all my experiments and projects I do for learning puproses.

### Tools

My tools. For now there is only one tool - Newsletter summarizer, which is under development.

## Licensing

This repository uses a dual licensing model:

### Code License

All code in this repository is licensed under the MIT License. This includes all source files, scripts, and configuration files. See [LICENSE-CODE](LICENSE-CODE) for details.

### Content License

All website content including blog posts, articles, documentation, images, and other media files in the `/website` directory is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

This means you are free to:

- Share — copy and redistribute the content in any medium or format
- Adapt — remix, transform, and build upon the content

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the content for commercial purposes.

For more details, see  [LICENSE-WEBSITE](./website/LICENSE-WEBSITE)

## Contributing

I welcome and appreciate contributions from the community! Here's how you can help:

- **Report bugs** by opening an issue
- **Suggest features** or improvements
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
