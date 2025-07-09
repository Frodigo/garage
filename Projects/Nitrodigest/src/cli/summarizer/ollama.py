"""
Ollama API implementation of the summarizer.
"""

import json
import requests
from typing import Dict, Any, Optional

from .base import BaseSummarizer
from .models import SummaryResult, ModelStatus
from .exceptions import (
    ConfigurationError,
    APIConnectionError,
    APIResponseError,
    ContentProcessingError,
    SummarizerError
)
from .utils.retry import retry
from .utils.token_budget_segmenter import TokenBudgetSegmenter
from .utils.simple_tokenizer import SimpleTokenizer
from .utils.preprocessors import preprocess


class OllamaSummarizer(BaseSummarizer):
    """Summarizer that uses a local Ollama instance"""

    def __init__(
        self,
        model: str = "mistral",
        ollama_api_url: str = "http://localhost:11434",
        timeout: int = 300,
        prompt_file: Optional[str] = None,
        max_tokens: int = 1500
    ):
        super().__init__(prompt_file)
        self.model = model
        self.ollama_api_url = ollama_api_url.rstrip('/')
        self.timeout = timeout
        self.max_tokens = max_tokens

        self.tokenizer = SimpleTokenizer(model_name=model)

        # Verify Ollama is available
        self._verify_ollama_availability()

    def _verify_ollama_availability(self) -> None:
        """
        Verify that Ollama is available.

        Raises:
            ConfigurationError: If Ollama is not available
        """
        try:
            response = requests.get(
                f"{self.ollama_api_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConfigurationError(
                    f"Ollama server returned status code "
                    f"{response.status_code}. "
                    "Make sure Ollama is running."
                )
        except requests.RequestException as e:
            raise ConfigurationError(
                f"Failed to connect to Ollama server at "
                f"{self.ollama_api_url}: {str(e)}"
            )

    def summarize(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SummaryResult:
        try:
            self._validate_input(content)
            content = preprocess(content)
            headers = self._prepare_headers()

            prompt = self.prompt.get_prompt()

            segmenter = TokenBudgetSegmenter(
                prompt=prompt,
                tokenizer=self.tokenizer.calculate_tokens,
                budget=self.max_tokens,
                language="english"
            )

            # Check if content needs to be chunked
            chunks = segmenter.create_chunks_with_sentences(content)

            if len(chunks) == 1:
                # Content fits within token budget
                prompt = self.prompt.format(content, metadata)
                data = self._prepare_request_data(prompt)

                self.logger.info(
                    f"Sending request to Ollama API "
                    f"using model {self.model}")

                # self.logger.info(f"Prompt: {prompt}")

                response = self.call_ollama_api(headers, data)
                self._check_response_status(response)
                response_data = response.json()
                summary = response_data["response"]
                tokens_used = response_data.get("eval_count", 0)
            else:
                # Content needs chunking
                self.logger.info(
                    f"Content exceeds token budget. "
                    f"Splitting into {len(chunks)} chunks.")

                intermediate_summaries = []
                total_tokens_used = 0

                # Process each chunk separately
                for i, chunk_with_prompt in enumerate(chunks):
                    self.logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                    # self.logger.info(f"Chunk: {chunk_with_prompt}")

                    data = self._prepare_request_data(chunk_with_prompt)
                    response = self.call_ollama_api(headers, data)
                    self._check_response_status(response)
                    response_data = response.json()

                    intermediate_summaries.append(response_data["response"])
                    total_tokens_used += response_data.get("eval_count", 0)

                # Combine intermediate summaries if necessary
                combined_summaries = " ".join(intermediate_summaries)
                summary = combined_summaries
                tokens_used = total_tokens_used

            return SummaryResult(
                status=ModelStatus.SUCCESS,
                summary=summary,
                model_used=self.model,
                tokens_used=tokens_used,
                metadata={"api_response": {"chunks_processed": len(chunks)}}
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
                f"{self.ollama_api_url}/api/generate",
                headers=headers,
                data=json.dumps(data),
                timeout=300
            )
        except requests.Timeout:
            raise APIConnectionError(
                "Request to Ollama API timed out after 300 seconds")
        except requests.ConnectionError:
            raise APIConnectionError(
                f"Failed to connect to Ollama API at {self.ollama_api_url}. "
                "Check if Ollama is running."
            )

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare request headers."""
        return {
            "Content-Type": "application/json"
        }
