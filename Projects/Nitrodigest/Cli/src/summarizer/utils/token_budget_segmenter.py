import nltk
from typing import Optional, Dict, Any
nltk.download('punkt_tab')

"""
 Split text to chunks based on token budget
"""


class TokenBudgetSegmenter:
    """A class to segment text into chunks based on a token budget.

    This class helps split text into manageable chunks while respecting a given
    token budget, ensuring that each chunk (including the prompt) stays within
    the specified limit.
    """

    def __init__(
            self,
            prompt: str,
            tokenizer,
            budget: int = 2048,
            language: str = "english"):
        """Initialize the TokenBudgetSegmenter.

        Args:
            prompt (str): The prompt to be used for tokenization.
            tokenizer (callable): A function that takes a string and returns
                the number of tokens.
            budget (int): The maximum number of tokens allowed in a chunk,
                including the prompt.
            language (str): The language of the text.

        Raises:
            ValueError: If the prompt length exceeds the budget.
        """
        self.tokenizer = tokenizer
        self.prompt = prompt
        self.budget = budget
        self.language = language
        self.prompt_tokens = self.tokenizer(prompt)

        if self.prompt_tokens > self.budget:
            raise ValueError(
                f"Prompt length {self.prompt_tokens} exceeds budget "
                f"{self.budget}. Please provide a shorter prompt."
            )

    def _split_text_to_sentences(self, text: str) -> list:
        """Split text into sentences.

        Args:
            text (str): The text to be split.

        Returns:
            list: A list of sentences.
        """
        return nltk.sent_tokenize(text, language=self.language)

    def create_chunks_with_sentences(
            self,
            text: str,
            metadata: Optional[Dict[str, Any]] = None
    ) -> list:
        """Create chunks of text based on the token budget.

        Args:
            text (str): The text to be chunked.
            metadata (Dict[str, Any], optional): Metadata to be included
                in the prompt.

        Returns:
            list: A list of chunks, each prefixed with the prompt.
        """
        sentences = self._split_text_to_sentences(text)
        available_budget = self.budget - self.prompt_tokens

        # Format metadata string
        metadata_str = ""
        if metadata:
            metadata_str = (
                f"This email is from: {metadata.get('from', 'Unknown')}\n"
                f"Subject: {metadata.get('subject', 'Unknown')}\n"
                f"Date: {metadata.get('date', 'Unknown')}\n"
            )

        chunks = []
        current_chunk = []
        current_chunk_tokens = 0

        for sentence in sentences:
            sentence_tokens = self.tokenizer(sentence)

            if current_chunk_tokens + sentence_tokens > available_budget:
                if current_chunk:
                    # Format the prompt with current chunk and metadata
                    chunk_text = " ".join(current_chunk)
                    processed_prompt = self.prompt.replace(
                        "{metadata}", metadata_str)
                    processed_prompt = processed_prompt.replace(
                        "{text}", chunk_text)
                    chunks.append(processed_prompt)
                current_chunk = [sentence]
                current_chunk_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_chunk_tokens += sentence_tokens

        if current_chunk:
            # Format the prompt with the last chunk and metadata
            chunk_text = " ".join(current_chunk)
            processed_prompt = self.prompt.replace("{metadata}", metadata_str)
            processed_prompt = processed_prompt.replace("{text}", chunk_text)
            chunks.append(processed_prompt)

        return chunks
