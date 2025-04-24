from summarizer.utils.token_budget_segmenter import TokenBudgetSegmenter
import pytest


class TestTokenBudgetSegmenter():

    short_prompt = "This is a short prompt."
    long_prompt = "This is a long prompt that exceeds the token budget set for the test case."

    def test_create_chunks_for_short_sentence(self):
        segmenter = TokenBudgetSegmenter(
            tokenizer=lambda x: x.split(),
            prompt=self.short_prompt,
            budget=100,
            language="english"
        )

        text = "This is a short sentence."
        expected_chunk = [
            f'{self.short_prompt}This is a short sentence.']
        result = segmenter.create_chunks(text)
        assert result == expected_chunk, f"Expected {expected_chunk}, but got {result}"

    def test_create_chunks_for_multiple_sentence(self):
        segmenter = TokenBudgetSegmenter(
            tokenizer=lambda x: x.split(),
            prompt=self.short_prompt,
            budget=10,
            language="english"
        )

        text = "This is a long sentence that exceeds the token budget set for the test case. This is another one"
        expected_chunk = [
            f'{self.short_prompt}This is a long sentence that exceeds the token budget set for the test case.',
            f'{self.short_prompt}This is another one']
        result = segmenter.create_chunks(text)
        assert result == expected_chunk, f"Expected {expected_chunk}, but got {result}"

    def test_raise_value_error_for_long_prompt(self):
        with pytest.raises(ValueError) as excinfo:
            TokenBudgetSegmenter(
                tokenizer=lambda x: x.split(),
                prompt=self.long_prompt,
                budget=10,
                language="english"
            )

        assert str(
            excinfo.value) == f"Prompt length {len(self.long_prompt.split())} exceeds budget 10. Please provide a shorter prompt."
