from typing import Self
from domain.entity.category import Category


class Product:
    def __init__(self, name: str, price: float, category: Category, available: bool = True):
        if name == None or name.strip() == None:
            raise ValueError("Product name cannot be empty")
        else:
            self.name = name

        if price < 0:
            raise ValueError("product price cannot be negative")
        else:
            self.price = price

        if category == None:
            raise ValueError("Progduct category cannot be empty")
        else:
            self.category = category

        self.available = available

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Product):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Product(name='{self.name}')"

    def __str__(self):
        return f"{self.name} ${self.price}"

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> str:
        return self.price

    def get_category(self) -> Category:
        return self.category

    def is_available(self) -> bool:
        return self.available

    def set_available(self, available: bool) -> Self:
        self.available = available

        return self
