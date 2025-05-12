#!/bin/bash
ollama serve &
sleep 5
ollama create nitroModel -f Modelfile
tail -f /dev/null
