from abc import ABC, abstractmethod
from typing import Dict
from domain import Product


class PromotionStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, products: Dict[Product, int]) -> float:
        pass

    @abstractmethod
    def get_promotion_code(self) -> str:
        pass
