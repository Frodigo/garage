from typing import Dict
from application import EmptyCartException, InvalidPromotionException, PromotionStrategy
from domain import Product


class PercentagePromotion(PromotionStrategy):
    DEFAULT_DISCOUNT_PERCENTAGE = 10.0

    def __init__(self, promotion_code: str, discount_percentage: float = None):
        if discount_percentage is None:
            discount_percentage = self.DEFAULT_DISCOUNT_PERCENTAGE

        if not promotion_code or promotion_code.strip() == "":
            raise InvalidPromotionException("Promotion code cannot be empty")
        else:
            self.promotion_code = promotion_code

        if discount_percentage < 0 or discount_percentage > 100:
            raise InvalidPromotionException(promotion_code,
                                            f"Discount percentage must be between 0 and 100, got: {discount_percentage}")
        else:
            self.discount_percentage = discount_percentage

    def calculate_discount(self, products: Dict[Product, int]) -> float:
        if products is None or not products:
            raise EmptyCartException(
                "Cannot calculate discount on an empty cart")

        total_price = sum(product.get_price() *
                          quantity for product, quantity in products.items())
        return total_price * (self.discount_percentage / 100.0)

    def get_promotion_code(self) -> str:
        return self.promotion_code
