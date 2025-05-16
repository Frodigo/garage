---
permalink: projects/nitrodigest/docs/getting-started/installation
---
NitroDigest is distributed as a Python package and it's available [here](https://pypi.org/project/nitrodigest-cli/). Before installing NitroDigest, **make sure you have Ollama installed** on your system (Ollama is the local LLM runtime NitroDigest uses). If you haven’t, download and install [Ollama](https://ollama.com/download) from the official site for your platform, and download the desired language model with `ollama pull <model>`. If you prefer running Ollama on Docker, you can use predefined docker-compsoe setup that is described [here](Ollama%20setup.md).

## Install from PyPi

If you already have **Python 3.6 or newer** installed, the fastest way to get started with NitroDigest is by installing it from [PyPI](https://pypi.org/project/nitrodigest-cli/):

### Step 1: Install via `pip`

```bash
pip install nitrodigest-cli
```

This installs the CLI tool globally and makes the nitrodigest command available in your terminal.

💡 **Tip:** If you’re using Python in a virtual environment or system-wide installation, make sure `pip` refers to Python 3. You can also use `pip3` if needed:

```bash
pip3 install nitrodigest-cli
```

### Step 2: Verify installation

After installing, run the following command to confirm everything works:

```bash
nitrodigest --help
```

You should see the CLI help output showing available options.

### Step 3: Play with it

You are ready to summarize a first text. Go to [Quickstart](Quickstart.md) page to see how to make it happen!

### Need to uninstall?

You can easily uninstall the tool by using one command:

```bash
pip uninstall nitrodigest-cli
```

---
## Install from source

If you prefer working with the latest source code, want to contribute, or need to modify NitroDigest, you can install it from the GitHub repository.

### Step 1: Clone the repository

```bash
git clone https://github.com/Frodigo/garage.git
cd garage/Projects/Nitrodigest/src/cli
```

### Step 2: (Optional) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install NitroDigest locally (editable mode)

```bash
pip install -e .
```

💡 **Tip:** Make sure, you are in nitrdigest directory (`Projects/Nitrodigest`) before you run this command

### Step 5: Verify installation

After installing, run the following command to confirm everything works:

```bash
nitrodigest --help
```

You should see the CLI help output showing available options.

### Step 6: Play with it

You are ready to summarize a first text. Go to [Quickstart](Quickstart.md) page to see how to make it happen!

---
Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs #PyPi #installation
