import time
import requests
from enum import Enum


class RetryStatusCode(Enum):
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


def retry(func):
    """
    Retries a function up to 2 times (for a total of 3 attempts, including the initial attempt)
    with 10-second delays on HTTP status codes 408, 409, 429, 500, 502, 503, 504 or request exceptions.
    """
    def wrapper(*args, **kwargs):
        max_retries = 2
        delay_seconds = 10
        retry_status_codes = {code.value for code in RetryStatusCode}

        for attempt in range(max_retries + 1):
                response = func(*args, **kwargs)

                if response.status_code not in retry_status_codes:
                    return response

                if attempt == retries:
                    return response

            except requests.exceptions.RequestException as e:
                if attempt == retries:
                    raise

            print(f"Attempt {attempt + 1} failed")
            time.sleep(delay_seconds)
            print("Retrying...")

    return wrapper
