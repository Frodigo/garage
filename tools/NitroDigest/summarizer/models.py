"""
Models module for the summarizer package.

This module defines data models and enums used throughout the summarizer package.
"""

from enum import Enum
from typing import Optional, Dict, Any


class ModelStatus(Enum):
    """Enum representing the status of a summarization operation"""
    SUCCESS = "success"
    ERROR = "error"


class SummaryResult:
    """Class to represent the result of a summarization operation"""

    def __init__(self,
                 status: ModelStatus,
                 summary: str = "",
                 error: Optional[Exception] = None,
                 model_used: str = "",
                 tokens_used: int = 0,
                 metadata: Optional[Dict[str, Any]] = None):
        self.status = status
        self.summary = summary
        self.error = error
        self.model_used = model_used
        self.tokens_used = tokens_used
        self.metadata = metadata or {}

    def is_success(self) -> bool:
        """Check if summarization was successful"""
        return self.status == ModelStatus.SUCCESS

    def __str__(self) -> str:
        """String representation of the result"""
        if self.is_success():
            return f"Summary successfully generated using {self.model_used} ({self.tokens_used} tokens)"
        return f"Summarization failed: {str(self.error)}"
