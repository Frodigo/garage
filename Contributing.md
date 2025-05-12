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
