import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

"""
 Split text to chunks based on token budget
"""


class TokenBudgetSegmenter:
    """
    A class to segment text into chunks based on a token budget.
    """

    def __init__(self, prompt: str, tokenizer: callable, budget: int = 4096, language: str = "english"):
        """
        Initialize the TokenBudgetSegmenter with a prompt, tokenizer and budget.

        Args:
            prompt (str): The prompt to be used for tokenization.
            tokenizer (callable): A function that takes a string and returns the number of tokens.
            budget (int): The maximum number of tokens allowed in a chunk, including the prompt
            language (str): The language of the text
        """
        self.tokenizer = tokenizer
        self.prompt = prompt
        self.budget = budget
        self.language = language
        self.prompt_tokens = self.tokenizer(prompt)
        self.prompt_len = len(self.prompt_tokens)

        if self.prompt_len > self.budget:
            raise ValueError(
                f"Prompt length {self.prompt_len} exceeds budget {self.budget}. "
                "Please provide a shorter prompt."
            )

    def _split_text_to_sentences(self, text: str):
        """
        Split text into sentences.

        Args:
            text (str): The text to be split.

        Returns:
            list: A list of sentences.
        """
        return nltk.sent_tokenize(text, language=self.language)

    def create_chunks(self, text: str):
        """
        Create chunks of text based on the token budget.

        Args:
            text (str): The text to be chunked.

        Returns:
            list: A list of chunks.
        """
        sentences = self._split_text_to_sentences(text)
        available_budget = self.budget - self.prompt_len

        chunks = []
        current_chunk = []
        current_chunk_tokens = 0

        for sentence in sentences:
            sentence_tokens = len(self.tokenizer(sentence))

            if current_chunk_tokens + sentence_tokens > available_budget:

                if len(current_chunk):
                    chunks.append(" ".join(current_chunk))

                current_chunk = [sentence]
                current_chunk_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_chunk_tokens += sentence_tokens

        if len(current_chunk):
            chunks.append(" ".join(current_chunk))

        # Combine each chunk with the prompt
        chunks_with_prompt = [self.prompt + chunk for chunk in chunks]

        return chunks_with_prompt
