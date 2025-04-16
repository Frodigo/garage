import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class SummarizerType(Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    OLLAMA = "ollama"


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
    type: SummarizerType
    model: Optional[str] = None
    base_url: str = "http://localhost:11434"
    api_key: Optional[str] = None
    timeout: int = 300

    def validate(self) -> None:
        if self.type == SummarizerType.OLLAMA and not self.model:
            raise ValueError("Model is required for Ollama")
        if (self.type in [SummarizerType.CLAUDE, SummarizerType.CHATGPT] and
                not self.api_key):
            raise ValueError("API key is required for Claude and ChatGPT")
        if self.timeout <= 0:
            raise ValueError("Timeout must be a positive number")


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

        if not self.summarizer.type:
            raise ValueError("Summarizer type is required")
        if (self.summarizer.type in [SummarizerType.CLAUDE,
                                     SummarizerType.CHATGPT] and
                not self.summarizer.api_key):
            raise ValueError("API key is required for Claude and ChatGPT")
        if (self.summarizer.type == SummarizerType.OLLAMA and
                not self.summarizer.model):
            raise ValueError("Model is required for Ollama")

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
        summarizer_type = SummarizerType(summarizer_data['type'])
        model = summarizer_data.get('model')
        if model is None:
            if summarizer_type == SummarizerType.CLAUDE:
                model = "claude-3-haiku-20240307"
            elif summarizer_type == SummarizerType.CHATGPT:
                model = "gpt-3.5-turbo"
            elif summarizer_type == SummarizerType.OLLAMA:
                model = "mistral"

        summarizer_config = SummarizerConfig(
            type=summarizer_type,
            model=model,
            base_url=summarizer_data.get('base_url', 'http://localhost:11434'),
            api_key=summarizer_data.get('api_key'),
            timeout=summarizer_data.get('timeout', 300)
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
                'type': self.summarizer.type.value,
                'model': self.summarizer.model,
                'base_url': self.summarizer.base_url,
                'timeout': self.summarizer.timeout
            },
            'summaries_path': self.summaries_path,
            'limit': self.limit,
            'mark_as_read': self.mark_as_read
        }

        if self.summarizer.api_key:
            data['summarizer']['api_key'] = self.summarizer.api_key

        return data

    def to_json(self, file_path: str) -> None:
        """Save the configuration to a JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
