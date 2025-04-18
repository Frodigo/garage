"""
Ollama API implementation of the summarizer.
"""

import json
import requests
from typing import Dict, Any, Optional

from summarizer.base import BaseSummarizer
from summarizer.models import SummaryResult, ModelStatus
from summarizer.exceptions import (
    ConfigurationError,
    APIConnectionError,
    APIResponseError,
    ContentProcessingError,
    SummarizerError
)
from summarizer.utils.retry import retry


class OllamaSummarizer(BaseSummarizer):
    """Summarizer that uses a local Ollama instance"""

    def __init__(
        self,
        model: str = "mistral",
        base_url: str = "http://localhost:11434",
        timeout: int = 300
    ):
        super().__init__()
        self.model = model
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        # Verify Ollama is available
        self._verify_ollama_availability()

    def _verify_ollama_availability(self) -> None:
        """
        Verify that Ollama is available.

        Raises:
            ConfigurationError: If Ollama is not available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConfigurationError(
                    f"Ollama server returned status code "
                    f"{response.status_code}. "
                    "Make sure Ollama is running."
                )
        except requests.RequestException as e:
            raise ConfigurationError(
                f"Failed to connect to Ollama server at "
                f"{self.base_url}: {str(e)}"
            )

    def summarize(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SummaryResult:
        try:
            self._validate_input(content)

            # First summarization
            headers = self._prepare_headers()
            prompt = self.prompt.format(content, metadata)
            data = self._prepare_request_data(prompt)

            self.logger.info(
                f"Sending first request to Ollama API "
                f"using model {self.model}")
            response = self.call_ollama_api(headers, data)
            self._check_response_status(response)
            response_data = response.json()
            first_summary = response_data["response"]

            # commented out for now to simplify
            # the process for debugging purposes
            # # Second summarization
            # second_prompt = self.prompt.format_second(first_summary)
            # data = self._prepare_request_data(second_prompt)

            # self.logger.info(
            #     f"Sending second request to Ollama API "
            #     f"using model {self.model}")
            # response = self.call_ollama_api(headers, data)
            # self._check_response_status(response)
            # response_data = response.json()
            # final_summary = response_data["response"]

            tokens_used = 0
            if "eval_count" in response_data:
                tokens_used = response_data.get("eval_count", 0)

            return SummaryResult(
                status=ModelStatus.SUCCESS,
                summary=first_summary,
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
                    f"Failed to connect to Ollama API: {str(e)}")
            )
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=SummarizerError(f"Unexpected error: {str(e)}")
            )

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
            "prompt": prompt,
            "stream": False
        }

    def _check_response_status(self, response: requests.Response) -> None:
        """
        Check response status and raise appropriate exceptions.

        Args:
            response: The response from the API

        Raises:
            APIResponseError: If the API returns an error response
        """
        if response.status_code == 200:
            return

        error_text = response.text

        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "error" in error_data:
                error_text = error_data.get("error", error_text)
        except json.JSONDecodeError:
            pass

        raise APIResponseError(response.status_code, error_text)

    @retry
    def call_ollama_api(
        self,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> requests.Response:
        """
        Call Ollama API with retry capability.

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
                f"{self.base_url}/api/generate",
                headers=headers,
                data=json.dumps(data),
                timeout=300
            )
        except requests.Timeout:
            raise APIConnectionError(
                "Request to Ollama API timed out after 300 seconds")
        except requests.ConnectionError:
            raise APIConnectionError(
                f"Failed to connect to Ollama API at {self.base_url}. "
                "Check if Ollama is running."
            )

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare request headers."""
        return {
            "Content-Type": "application/json"
        }
