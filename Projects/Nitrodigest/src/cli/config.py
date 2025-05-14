import json
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Config:
    model: str = 'mistral'
    ollama_api_url: str = "http://localhost:11434"
    timeout: int = 300
    prompt_file: Optional[str] = 'prompt_template.txt'

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create a Config instance from a dictionary"""
        return cls(
            model=data.get('model', 'mistral'),
            ollama_api_url=data.get(
                'ollama_api_url', 'http://localhost:11434'),
            timeout=data.get('timeout', 300),
            prompt_file=data.get('prompt_file', 'prompt_template.txt'),
        )

    @classmethod
    def from_json(cls, file_path: str) -> 'Config':
        """Load configuration from a JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary"""
        data = {
            'model': self.model,
            'ollama_api_url': self.ollama_api_url,
            'timeout': self.timeout,
        }

        if self.prompt_file:
            data['prompt_file'] = self.prompt_file

        return data

    def to_json(self, file_path: str) -> None:
        """Save the configuration to a JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
