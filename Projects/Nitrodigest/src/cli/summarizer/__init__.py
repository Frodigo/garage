"""
Summarizer package for generating summaries from text using various LLM providers.
"""

from .base import BaseSummarizer
from .models import SummaryResult, ModelStatus
from .exceptions import (
    SummarizerError,
    ConfigurationError,
    APIConnectionError,
    APIResponseError,
    APIAuthenticationError,
    APIRateLimitError,
    ContentProcessingError
)

from .ollama import OllamaSummarizer
from .prompt import Prompt

__all__ = [
    'BaseSummarizer',
    'SummaryResult',
    'ModelStatus',
    'SummarizerError',
    'ConfigurationError',
    'APIConnectionError',
    'APIResponseError',
    'APIAuthenticationError',
    'APIRateLimitError',
    'ContentProcessingError',
    'OllamaSummarizer',
    'Prompt',
]
