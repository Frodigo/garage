# NitroWebfetch

Extract web content, cleanly.

**NitroWebfetch – the developer‑friendly web content extractor with CSS selectors.**

This project is in alpha phase.

## Features

- Extracts content from web pages using CSS selectors
- Converts HTML to clean Markdown format
- Fallback selectors for maximum compatibility
- Command-line interface with various options
- Built on Playwright for reliable web scraping
- Completely free (open source, MIT license)

## Ideas for next steps

- Add support for multiple output formats (JSON, plain text)
- Batch processing for multiple URLs
- Custom user-agent and headers configuration
- Integration with NitroDigest for web page summarization
- Support for authentication and cookies
- Content filtering and cleaning options

---

## Usage

### Prerequisites

To run this tool, you need to have [Python](https://www.python.org/downloads/) installed on your local machine.

### Installation

Install NitroWebfetch via pip:

```bash
pip install nitrowebfetch-cli
playwright install firefox
```

For development installation:

```bash
cd Projects/Nitrowebfetch
pip install -e .
playwright install firefox
```

### Basic Usage

Run NitroWebfetch to extract content from web pages:

```bash
nitrowebfetch <url> > <output_file>
```

#### Examples

Extract article content from a webpage and save it to a file:

```bash
nitrowebfetch https://example.com/article > article.md
```

Extract content using a custom CSS selector:

```bash
nitrowebfetch https://example.com --selector ".main-content" > content.md
```

Get HTML output instead of Markdown:

```bash
nitrowebfetch https://example.com --format html > content.html
```

### Command Line Arguments

You can customize the extraction process using command line arguments:

```bash
nitrowebfetch \
    --selector ".article-body" \
    --format md \
    https://example.com
```

Available arguments:

- `url`: URL to fetch content from (required)
- `--selector`: CSS selector to use for content extraction (default: article)
- `--format`: Format of output content - 'md' for Markdown or 'html' for raw HTML (default: md)

### Fallback Selectors

If the primary selector doesn't match any elements, NitroWebfetch automatically tries these alternatives:

- `article`
- `main`
- `.article`
- `.content`
- `#content`
- `.post`
- `.entry-content`

---

## Contributing

Do you want to contribute to this tool? Check the Contributing page:

[Getting started](../../Contributing.md)

## Report an issue

Found an issue? You can easily report it here:

[https://github.com/Frodigo/garage/issues/new](https://github.com/Frodigo/garage/issues/new)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
