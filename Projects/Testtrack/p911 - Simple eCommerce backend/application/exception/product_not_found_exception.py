from typing import Optional, Union


class ProductNotFoundException(Exception):
    def __init__(self, message_or_id: Union[str, int],
                 additional_info_or_cause: Optional[Union[str,
                                                          Exception]] = None,
                 cause: Optional[Exception] = None):
        if isinstance(message_or_id, int):
            message = f"Product with ID {message_or_id} not found"
            super().__init__(message)
            self.__cause__ = additional_info_or_cause if isinstance(
                additional_info_or_cause, Exception) else cause
        elif isinstance(additional_info_or_cause, str):
            message = f"Product with name '{message_or_id}' not found. {additional_info_or_cause}"
            super().__init__(message)
            self.__cause__ = cause
        else:
            super().__init__(message_or_id)
            self.__cause__ = additional_info_or_cause if isinstance(
                additional_info_or_cause, Exception) else cause
