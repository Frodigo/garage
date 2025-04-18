"""
Base module for the summarizer package.

This module defines the base summarizer class that all specific
summarizer implementations should inherit from.
"""

import logging
from typing import Optional, Dict, Any

from prompt import Prompt
from summarizer.models import SummaryResult
from summarizer.utils.logging import get_logger

logger = get_logger(__name__)


class BaseSummarizer:
    """Base class for all summarizers"""

    def __init__(self):
        self.prompt = Prompt()
        self.logger = logger.getChild(self.__class__.__name__)

    def summarize(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> SummaryResult:
        """
        Summarize the given text.

        Args:
            text: The text to summarize
            metadata: Optional metadata about the text

        Returns:
            A SummaryResult object containing the result of the summarization
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _validate_input(self, text: str) -> None:
        """
        Validate the input text.

        Args:
            text: The text to validate

        Raises:
            ValueError: If the text is invalid
        """
        if not text:
            raise ValueError("Input text cannot be empty")
