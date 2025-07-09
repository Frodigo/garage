import emoji
import re


def _remove_emojis(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')

    return text


def _remove_email_addresses(text: str) -> str:
    email_pattern = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.sub('', text)


def _remove_phone_numbers(text: str) -> str:
    phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    return phone_pattern.sub('', text)


def _remove_urls(text: str) -> str:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)


def _remove_special_chars(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s.,!?;:()\'\-]', '', text)


def _remove_extra_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def preprocess(text: str) -> str:
    text = _remove_emojis(text)
    text = _remove_email_addresses(text)
    text = _remove_phone_numbers(text)
    text = _remove_urls(text)
    text = _remove_special_chars(text)
    text = _remove_extra_whitespace(text)

    return text
