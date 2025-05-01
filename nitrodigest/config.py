import json
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EmailConfig:
    address: str
    password: str
    server: str = "imap.gmail.com"
    port: int = 993
    folder: str = "INBOX"

    def validate(self) -> None:
        if not self.address or not self.password:
            raise ValueError("Email address and password are required")
        if not self.server:
            raise ValueError("IMAP server is required")


@dataclass
class SummarizerConfig:
    model: Optional[str] = 'mistral'
    base_url: str = "http://localhost:11434"
    timeout: int = 300
    prompt_file: Optional[str] = 'prompt_template.txt'

    def validate(self) -> None:
        if not self.model:
            raise ValueError("Model is required for Ollama")
        if self.timeout <= 0:
            raise ValueError("Timeout must be a positive number")
        if (self.prompt_file and
                not os.path.exists(self.prompt_file)):
            raise ValueError(
                f"Prompt file not found: {self.prompt_file}")


@dataclass
class Config:
    email: EmailConfig
    summarizer: SummarizerConfig
    summaries_path: str = "summaries"
    limit: int = 5
    mark_as_read: bool = True

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.email.address:
            raise ValueError("Email address is required")
        if not self.email.password:
            raise ValueError("Email password is required")
        if not self.email.server:
            raise ValueError("IMAP server is required")
        if not self.email.port:
            raise ValueError("IMAP port is required")
        if not self.email.folder:
            raise ValueError("Email folder is required")

        self.email.validate()
        self.summarizer.validate()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create a Config instance from a dictionary"""
        email_config = EmailConfig(
            address=data['email']['address'],
            password=data['email']['password'],
            server=data['email'].get('server', 'imap.gmail.com'),
            port=data['email'].get('port', 993),
            folder=data['email'].get('folder', 'INBOX')
        )

        summarizer_data = data['summarizer']
        model = summarizer_data.get('model')
        if model is None:
            model = "mistral"

        summarizer_config = SummarizerConfig(
            model=model,
            base_url=summarizer_data.get('base_url', 'http://localhost:11434'),
            timeout=summarizer_data.get('timeout', 300),
            prompt_file=summarizer_data.get(
                'prompt_file', 'prompt_template.txt'),
        )

        return cls(
            email=email_config,
            summarizer=summarizer_config,
            summaries_path=data.get('summaries_path', 'summaries'),
            limit=data.get('limit', 5),
            mark_as_read=data.get('mark_as_read', True)
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
            'email': {
                'address': self.email.address,
                'password': self.email.password,
                'server': self.email.server,
                'port': self.email.port,
                'folder': self.email.folder
            },
            'summarizer': {
                'model': self.summarizer.model,
                'base_url': self.summarizer.base_url,
                'timeout': self.summarizer.timeout
            },
            'summaries_path': self.summaries_path,
            'limit': self.limit,
            'mark_as_read': self.mark_as_read
        }

        if self.summarizer.prompt_file:
            data['summarizer']['prompt_file'] = self.summarizer.prompt_file

        return data

    def to_json(self, file_path: str) -> None:
        """Save the configuration to a JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
