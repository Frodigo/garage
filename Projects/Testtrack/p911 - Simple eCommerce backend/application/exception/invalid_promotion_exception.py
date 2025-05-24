from typing import Optional


class InvalidPromotionException(Exception):
    def __init__(self, message_or_code: str, reason_or_cause: Optional[str] = None,
                 cause: Optional[Exception] = None):
        if reason_or_cause is not None and isinstance(reason_or_cause, str):
            message = f"Invalid promotion code '{message_or_code}': {reason_or_cause}"
            super().__init__(message)
            self.__cause__ = cause
        else:
            super().__init__(message_or_code)
            self.__cause__ = reason_or_cause if isinstance(
                reason_or_cause, Exception) else cause
