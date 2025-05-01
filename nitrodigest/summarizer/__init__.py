"""
Summarizer package for generating summaries from text using various LLM providers.
"""

from summarizer.base import BaseSummarizer
from summarizer.models import SummaryResult, ModelStatus
from summarizer.exceptions import (
    SummarizerError,
    ConfigurationError,
    APIConnectionError,
    APIResponseError,
    APIAuthenticationError,
    APIRateLimitError,
    ContentProcessingError
)

from nitrodigest.summarizer.ollama import OllamaSummarizer

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
    'OllamaSummarizer'
]
