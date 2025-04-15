"""
Exceptions module for the summarizer package.

This module defines a hierarchy of exceptions used throughout the summarizer package.
"""


class SummarizerError(Exception):
    """Base exception class for summarizer errors"""
    pass


class ConfigurationError(SummarizerError):
    """Raised when there's an issue with the configuration"""
    pass


class APIConnectionError(SummarizerError):
    """Raised when there's an issue connecting to the API"""
    pass


class APIResponseError(SummarizerError):
    """Raised when the API returns an error response"""

    def __init__(self, status_code: int, response_text: str, *args):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(
            f"API returned error status {status_code}: {response_text}", *args)


class APIAuthenticationError(APIResponseError):
    """Raised when there's an authentication issue with the API"""
    pass


class APIRateLimitError(APIResponseError):
    """Raised when the API rate limit is exceeded"""
    pass


class ContentProcessingError(SummarizerError):
    """Raised when there's an issue processing the content"""
    pass
