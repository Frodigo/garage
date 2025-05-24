from abc import ABC, abstractmethod
from typing import List
from domain.entity.category import Category
from domain.entity.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_products_sorted_alphabetically(self) -> List[Product]:
        pass

    @abstractmethod
    def get_available_products_by_category(self, category: Category) -> List[Product]:
        pass
