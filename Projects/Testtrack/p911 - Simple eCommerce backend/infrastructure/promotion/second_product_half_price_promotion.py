from typing import Dict
from application import PromotionStrategy
from domain import Product


class SecondProductHalfPricePromotion(PromotionStrategy):
    DISCOUNT_PERCENTAGE = 50.0

    def __init__(self, promotion_code: str):
        if not promotion_code or promotion_code.strip() == "":
            raise ValueError("Promotion code cannot be empty")
        else:
            self.promotion_code = promotion_code

    def calculate_discount(self, products: Dict[Product, int]) -> float:
        if not products:
            return 0

        total_discount = 0
        for product, quantity in products.items():
            pairs = quantity // 2
            total_discount += pairs * \
                (product.get_price() * self.DISCOUNT_PERCENTAGE / 100.0)

        return total_discount

    def get_promotion_code(self) -> str:
        return self.promotion_code
