"""
OpenAI API implementation of the summarizer.
"""

import os
import json
import requests
from typing import Dict, Any, Optional

from summarizer.base import BaseSummarizer
from summarizer.models import SummaryResult, ModelStatus
from summarizer.exceptions import (
    ConfigurationError,
    APIConnectionError,
    APIResponseError,
    APIAuthenticationError,
    APIRateLimitError,
    ContentProcessingError,
    SummarizerError
)
from summarizer.utils.retry import retry


class ChatGPTSummarizer(BaseSummarizer):
    """Summarizer that uses OpenAI's ChatGPT API"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

        if not self.api_key:
            raise ConfigurationError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

    def summarize(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> SummaryResult:
        """
        Summarize text using OpenAI API.

        Args:
            text: The text to summarize
            metadata: Optional metadata about the text

        Returns:
            A SummaryResult object containing the result of the summarization
        """
        try:
            self._validate_input(text)

            headers = self._prepare_headers()
            prompt = self.prompt.format(text, metadata)
            data = self._prepare_request_data(prompt)

            self.logger.info(
                f"Sending request to OpenAI API using model {self.model}")
            response = self.call_openai_api(headers, data)

            self._check_response_status(response)

            response_data = response.json()
            summary = response_data["choices"][0]["message"]["content"]

            tokens_used = 0
            if "usage" in response_data:
                tokens_used = response_data["usage"].get("total_tokens", 0)

            return SummaryResult(
                status=ModelStatus.SUCCESS,
                summary=summary,
                model_used=self.model,
                tokens_used=tokens_used,
                metadata={"api_response": response_data}
            )

        except SummarizerError as e:
            self.logger.error(f"Summarizer error: {str(e)}", exc_info=True)
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=e
            )
        except ValueError as e:
            self.logger.error(f"Validation error: {str(e)}", exc_info=True)
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=ContentProcessingError(str(e))
            )
        except requests.RequestException as e:
            self.logger.error(f"Request error: {str(e)}", exc_info=True)
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=APIConnectionError(
                    f"Failed to connect to OpenAI API: {str(e)}")
            )
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=SummarizerError(f"Unexpected error: {str(e)}")
            )

    def _prepare_headers(self) -> Dict[str, str]:
        """
        Prepare request headers.

        Returns:
            A dictionary of headers for the API request
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _prepare_request_data(self, prompt: str) -> Dict[str, Any]:
        """
        Prepare request data.

        Args:
            prompt: The prompt to send to the API

        Returns:
            A dictionary of data for the API request
        """
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarizes newsletter content."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }

    def _check_response_status(self, response: requests.Response) -> None:
        """
        Check response status and raise appropriate exceptions.

        Args:
            response: The response from the API

        Raises:
            APIAuthenticationError: If authentication fails
            APIRateLimitError: If rate limit is exceeded
            APIResponseError: For other API errors
        """
        if response.status_code == 200:
            return

        error_text = response.text

        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "error" in error_data:
                error_text = error_data["error"].get("message", error_text)
        except:
            pass

        if response.status_code == 401:
            raise APIAuthenticationError(
                response.status_code, "Authentication failed. Check your API key.")
        elif response.status_code == 429:
            raise APIRateLimitError(
                response.status_code, "Rate limit exceeded. Try again later.")
        else:
            raise APIResponseError(response.status_code, error_text)

    @retry
    def call_openai_api(self, headers: Dict[str, str], data: Dict[str, Any]) -> requests.Response:
        """
        Call OpenAI API with retry capability.

        Args:
            headers: The headers for the API request
            data: The data for the API request

        Returns:
            The response from the API

        Raises:
            APIConnectionError: If there's an issue connecting to the API
        """
        try:
            return requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
        except requests.Timeout:
            raise APIConnectionError(
                "Request to OpenAI API timed out after 30 seconds")
        except requests.ConnectionError:
            raise APIConnectionError(
                "Failed to connect to OpenAI API. Check your internet connection.")
