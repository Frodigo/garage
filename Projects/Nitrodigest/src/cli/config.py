import json
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Config:
    def __init__(
        self,
        model: str = 'mistral',
        ollama_api_url: str = "http://localhost:11434",
        timeout: int = 300,
        prompt_file: Optional[str] = 'prompt_template.txt'
    ) -> None:
        self.ollama_api_url = ollama_api_url.rstrip('/')
        self.timeout = timeout if timeout is not None else 300
        self.prompt_file = prompt_file
        self.model = model
        self.validate()

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.model:
            raise ValueError("Model is required")
        if self.timeout <= 0:
            raise ValueError("Timeout must be a positive number")
        if (self.prompt_file and
                not os.path.exists(self.prompt_file)):
            raise ValueError(
                f"Prompt file not found: {self.prompt_file}")
