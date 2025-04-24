from summarizer.utils.token_budget_segmenter import TokenBudgetSegmenter
import pytest


class TestTokenBudgetSegmenter():

    short_prompt = "This is a short prompt. {metadata}{text}"
    long_prompt = ("This is a long prompt that exceeds the token budget "
                   "set for the test case.")

    def test_create_chunks_for_short_sentence(self):
        segmenter = TokenBudgetSegmenter(
            tokenizer=lambda x: len(x.split()),
            prompt=self.short_prompt,
            budget=100,
            language="english"
        )

        text = "This is a short sentence."
        expected_chunk = [
            'This is a short prompt. This is a short sentence.']
        result = segmenter.create_chunks_with_sentences(text)
        assert (result == expected_chunk), \
            f"Expected {expected_chunk}, but got {result}"

    def test_create_chunks_for_multiple_sentence(self):
        segmenter = TokenBudgetSegmenter(
            tokenizer=lambda x: len(x.split()),
            prompt=self.short_prompt,
            budget=10,
            language="english"
        )

        text = ("This is a long sentence that exceeds the token budget set "
                "for the test case. This is another one")
        expected_chunk = [
            'This is a short prompt. This is a long sentence that exceeds '
            'the token budget set for the test case.',
            'This is a short prompt. This is another one']
        result = segmenter.create_chunks_with_sentences(text)
        assert (result == expected_chunk), \
            f"Expected {expected_chunk}, but got {result}"

    def test_raise_value_error_for_long_prompt(self):
        with pytest.raises(ValueError) as excinfo:
            TokenBudgetSegmenter(
                tokenizer=lambda x: len(x.split()),
                prompt=self.long_prompt,
                budget=10,
                language="english"
            )

        error_msg = (f"Prompt length {len(self.long_prompt.split())} "
                     f"exceeds budget 10. Please provide a shorter prompt.")
        assert str(excinfo.value) == error_msg

    def test_create_chunks_with_metadata(self):
        segmenter = TokenBudgetSegmenter(
            tokenizer=lambda x: len(x.split()),
            prompt=self.short_prompt,
            budget=100,
            language="english"
        )

        text = "This is the email content."
        metadata = {
            "from": "test@example.com",
            "subject": "Test Email",
            "date": "2023-01-01"
        }

        metadata_str = ("This email is from: test@example.com\n"
                        "Subject: Test Email\n"
                        "Date: 2023-01-01\n")

        # Build expected result manually to avoid long lines
        prompt_part = "This is a short prompt. "
        expected = prompt_part + metadata_str + text
        expected_result = [expected]

        result = segmenter.create_chunks_with_sentences(text, metadata)
        assert (result == expected_result), \
            f"Expected {expected_result}, but got {result}"
