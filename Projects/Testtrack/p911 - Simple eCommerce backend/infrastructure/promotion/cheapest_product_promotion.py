from typing import Dict, List
from application import PromotionStrategy
from domain import Product


class CheapestProductPromotion(PromotionStrategy):
    DEFAULT_PRODUCTS_REQUIRED = 3
    DEFAULT_SPECIAL_PRICE = 1.0

    def __init__(self, promotion_code: str, special_price: float = None, products_required: int = None):
        if special_price is None:
            special_price = self.DEFAULT_SPECIAL_PRICE
        if products_required is None:
            products_required = self.DEFAULT_PRODUCTS_REQUIRED

        if not promotion_code or promotion_code.strip() == "":
            raise ValueError("Promotion code cannot be empty")
        else:
            self.promotion_code = promotion_code

        if special_price < 0:
            raise ValueError("Special price cannot be negative")
        else:
            self.special_price = special_price

        if products_required < 2:
            raise ValueError("Products required must be at least 2")
        else:
            self.products_required = products_required

    def calculate_discount(self, products: Dict[Product, int]) -> float:
        if not products:
            return 0

        all_products: List[Product] = []
        for product, quantity in products.items():
            for _ in range(quantity):
                all_products.append(product)

        if len(all_products) < self.products_required:
            return 0

        all_products.sort(key=lambda p: p.get_price())

        total_discount = 0
        for i in range(len(all_products)):
            if (i + 1) % self.products_required == 0:
                discounted_product = all_products[i]
                product_discount = discounted_product.get_price() - self.special_price
                if product_discount > 0:
                    total_discount += product_discount

        return total_discount

    def get_promotion_code(self) -> str:
        return self.promotion_code
