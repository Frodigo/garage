"""
A simple tokenizer implementation that doesn't require external dependencies.
"""


class SimpleTokenizer:
    """
    A simple tokenizer implementation
    that uses a pre-defined token ratio for each model.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    def calculate_tokens(self, text: str) -> int:
        """
        Calculate the number of tokens in a text using the model.
        """
        token_ratios = {
            "llama2": 0.25,   # ~4 characters per token
            "mistral": 0.23,  # ~4.3 characters per token
            "mpt": 0.22,      # ~4.5 characters per token
            "falcon": 0.26    # ~3.8 characters per token
        }

        ratio = token_ratios.get(self.model_name.lower(), 0.25)

        return int(len(text) * ratio)
