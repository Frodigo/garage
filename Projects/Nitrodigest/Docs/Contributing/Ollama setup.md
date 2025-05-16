---
permalink: projects/nitrodigest/docs/
---
### Prerequisites

- Docker and Docker Compose installed on your system
- Sufficient disk space (at least 10GB recommended, ideally 20% of your total disk space)
- For optimal performance: At least 8GB of RAM
- Optional for enhanced performance: NVIDIA GPU with proper drivers (for GPU acceleration)

### Run Ollama on docker using predefined docker compose

In the `ollama` directory you can find a `docker-compose.ollama.yml` file which contains setup
for `Olama` and `Open WebUI`.

1. To start Ollama run:

```bash
cd ollama
docker-compose -f docker-compose.ollama.yml up
```

Note that first build could take some time (~10-20min - depending on the internet connection)

1. Access the Ollama API directly at [http://localhost:11434](http://localhost:11434) or the web interface at [http://localhost:3000](http://localhost:11434)

Note: make sure that you have correct configuration in your `config.json` or `.env` file.

### Installing new models

If you want to install new models you have three options.

1. Update the Modelfile
2. Using the command line
3. Using the Web UI

#### Updating the Modelfile

1. Modify ollama/Modelfile and change model there.
2. Rebuild the container`

#### Using the command line

1. Access the Ollama container:

```bash
docker exec -it ollama /bin/bash
```

1. Pull a model:

```bash
ollama pull llama2
```

Replace "llama2" with any model you want to use (e.g., deepseek-r1, llava-phi3)

1. Run the model:

```bash
ollama run llama2
```

#### Using the Web UI

1. Navigate to [http://localhost:3000](http://localhost:3000) in your browser.
2. Create an account if prompted.
3. Go to the Models section and select "Pull a model from Ollama.com"
4. Choose from available models like llama2, deepseek-coder, etc.

---
Found an issue? Report a bug: <https://github.com/Frodigo/garage/issues/new>

#NitroDigest #Docs #NitroDigestDocs #Ollama #Docker
