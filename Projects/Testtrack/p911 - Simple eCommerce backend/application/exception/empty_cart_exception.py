from typing import Optional


class EmptyCartException(Exception):
    def __init__(self, message: str = "Operation cannot be performed on an empty shopping cart",
                 cause: Optional[Exception] = None):
        super().__init__(message)
        self.__cause__ = cause
