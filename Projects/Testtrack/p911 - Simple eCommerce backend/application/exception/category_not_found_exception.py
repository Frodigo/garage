from typing import Optional


class CategoryNotFoundException(Exception):
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.__cause__ = cause

    @classmethod
    def for_id(cls, category_id: int) -> 'CategoryNotFoundException':
        return cls(f"Category with ID {category_id} not found")

    @classmethod
    def for_name(cls, category_name: str, exact_match: bool = False) -> 'CategoryNotFoundException':
        message = f"Category with name '{category_name}' not found"
        if exact_match:
            message += " (exact match)"
        return cls(message)
