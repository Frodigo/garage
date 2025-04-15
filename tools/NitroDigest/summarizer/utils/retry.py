"""
Retry utilities for the summarizer package.
"""

import time
import logging
import functools
from typing import Callable, Any, Type, Tuple, Optional

logger = logging.getLogger(__name__)


def retry(
    func: Optional[Callable] = None,
    *,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    max_tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    logger_name: Optional[str] = None
) -> Callable:
    """
    Retry decorator with exponential backoff for the specified exceptions.

    Args:
        func: The function to decorate
        exceptions: The exceptions to catch and retry
        max_tries: The maximum number of attempts
        delay: The initial delay between retries in seconds
        backoff: The backoff multiplier
        logger_name: The name of the logger to use

    Returns:
        The decorated function
    """
    def decorator_retry(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper_retry(*args: Any, **kwargs: Any) -> Any:
            # Get logger
            log = logger
            if logger_name:
                log = logging.getLogger(logger_name)

            # Initialize variables for retry mechanism
            mtries, mdelay = max_tries, delay

            # Try call function until max_tries or success
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    # Don't retry certain types of exceptions
                    # Add any exceptions that should not be retried
                    non_retryable = []
                    for err_type in non_retryable:
                        if isinstance(e, err_type):
                            log.warning(f"Non-retryable error: {str(e)}")
                            raise e

                    msg = f"Retrying in {mdelay} seconds due to: {str(e)}"
                    log.warning(msg)

                    # Wait before next retry
                    time.sleep(mdelay)

                    # Update counters for next iteration
                    mtries -= 1
                    mdelay *= backoff

            # Final attempt
            return f(*args, **kwargs)

        return wrapper_retry

    # This handles both @retry and @retry(...)
    if func is None:
        return decorator_retry
    return decorator_retry(func)
