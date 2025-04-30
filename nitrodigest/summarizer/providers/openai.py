"""
OpenAI API implementation of the summarizer.
"""

import json
import requests
from typing import Dict, Any, Optional

from summarizer.base import BaseSummarizer
from summarizer.models import SummaryResult, ModelStatus
from summarizer.exceptions import (
    APIConnectionError,
    APIResponseError,
    APIAuthenticationError,
    APIRateLimitError
)
from summarizer.utils.retry import retry


class ChatGPTSummarizer(BaseSummarizer):
    """Summarizer that uses OpenAI's ChatGPT API"""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        timeout: int = 300,
        prompt_file: Optional[str] = None
    ):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        if prompt_file:
            self.prompt.set_template_path(prompt_file)

    def summarize(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SummaryResult:
        try:
            headers = self._prepare_headers()
            prompt = self.prompt.format(content, metadata)
            data = self._prepare_request_data(prompt)

            self.logger.info(
                f"Sending request to OpenAI API using model {self.model}")
            response = self.call_openai_api(headers, data)

            response_data = response.json()

            summary = response_data["choices"][0]["message"]["content"]

            tokens_used = 0
            if "usage" in response_data:
                tokens_used = response_data["usage"].get("total_tokens", 0)

            self._check_response_status(response)

            response_data = response.json()

            return SummaryResult(
                status=ModelStatus.SUCCESS,
                summary=summary,
                model_used=self.model,
                tokens_used=tokens_used,
                metadata={"api_response": response_data}
            )

        except Exception as e:
            return SummaryResult(
                status=ModelStatus.ERROR,
                error=APIConnectionError(str(e)),
                model_used=self.model
            )

    def _prepare_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _prepare_request_data(self, prompt: str) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }

    def _check_response_status(self, response: requests.Response) -> None:
        if response.status_code == 200:
            return

        error_text = response.text

        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "error" in error_data:
                error_text = error_data["error"].get("message", error_text)
        except json.JSONDecodeError:
            pass

        if response.status_code == 401:
            raise APIAuthenticationError(
                response.status_code,
                "Authentication failed. Check your API key."
            )
        elif response.status_code == 429:
            raise APIRateLimitError(
                response.status_code,
                "Rate limit exceeded. Try again later."
            )
        else:
            raise APIResponseError(response.status_code, error_text)

    @retry
    def call_openai_api(
        self,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> requests.Response:
        try:
            return requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
        except requests.Timeout:
            raise APIConnectionError(
                f"Request to OpenAI API timed out after {self.timeout} "
                "seconds"
            )
        except requests.ConnectionError:
            raise APIConnectionError(
                "Failed to connect to OpenAI API. Check your internet "
                "connection."
            )
