from summarizer import BaseSummarizer, ClaudeSummarizer, ChatGPTSummarizer, OllamaSummarizer
import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBaseSummarizer(unittest.TestCase):

    def test_base_summarizer_interface(self):
        summarizer = BaseSummarizer()
        with self.assertRaises(NotImplementedError):
            summarizer.summarize("test text")


class TestClaudeSummarizer(unittest.TestCase):

    @patch.dict('os.environ', {"ANTHROPIC_API_KEY": "fake-api-key"})
    def test_init_with_env_var(self):
        summarizer = ClaudeSummarizer()
        self.assertEqual(summarizer.api_key, "fake-api-key")

    def test_init_with_explicit_key(self):
        summarizer = ClaudeSummarizer(api_key="explicit-key")
        self.assertEqual(summarizer.api_key, "explicit-key")

    @patch.dict('os.environ', {}, clear=True)
    def test_init_without_key(self):
        with self.assertRaises(ValueError):
            ClaudeSummarizer()

    @patch('requests.post')
    def test_summarize_success(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"text": "Summarized text"}]}
        mock_post.return_value = mock_response

        # Test
        summarizer = ClaudeSummarizer(api_key="test-key")
        result = summarizer.summarize("Test content")

        # Verify
        self.assertEqual("Summarized text", result)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_summarize_empty_text(self, mock_post):
        summarizer = ClaudeSummarizer(api_key="test-key")
        result = summarizer.summarize("")

        self.assertEqual("", result)
        mock_post.assert_not_called()


class TestChatGPTSummarizer(unittest.TestCase):

    @patch.dict('os.environ', {"OPENAI_API_KEY": "fake-api-key"})
    def test_init_with_env_var(self):
        summarizer = ChatGPTSummarizer()
        self.assertEqual(summarizer.api_key, "fake-api-key")

    @patch('requests.post')
    def test_summarize_success(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [
            {"message": {"content": "Summarized text"}}]}
        mock_post.return_value = mock_response

        # Test
        summarizer = ChatGPTSummarizer(api_key="test-key")
        result = summarizer.summarize("Test content")

        # Verify
        self.assertEqual("Summarized text", result)
        mock_post.assert_called_once()


class TestOllamaSummarizer(unittest.TestCase):

    def test_init_default_values(self):
        summarizer = OllamaSummarizer()
        self.assertEqual(summarizer.model, "mistral")
        self.assertEqual(summarizer.base_url, "http://localhost:11434")

    def test_init_custom_values(self):
        summarizer = OllamaSummarizer(
            model="llama", base_url="http://custom-url:8000")
        self.assertEqual(summarizer.model, "llama")
        self.assertEqual(summarizer.base_url, "http://custom-url:8000")

    @patch('requests.post')
    def test_summarize_success(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Summarized text"}
        mock_post.return_value = mock_response

        # Test
        summarizer = OllamaSummarizer()
        result = summarizer.summarize("Test content")

        # Verify
        self.assertEqual("Summarized text", result)
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
