from typing import Dict, Optional
from application.exception.empty_cart_exception import EmptyCartException
from application.exception.product_unavailable_exception import ProductUnavailableException
from application.port.promotion_strategy import PromotionStrategy
from domain import Product


class ShoppingCartService:
    def __init__(self):
        self.products: Dict[Product, int] = {}
        self.active_promotion: Optional[PromotionStrategy] = None

    def add_product(self, product: Product) -> None:
        if product is None:
            raise ValueError("Product cannot be null")
        if not product.is_available():
            raise ProductUnavailableException(product)

        self.products[product] = self.products.get(product, 0) + 1

    def remove_product(self, product: Product) -> None:
        if product is None:
            raise ValueError("Product cannot be null")
        if product not in self.products:
            return

        quantity = self.products[product]
        if quantity > 1:
            self.products[product] = quantity - 1
        else:
            del self.products[product]

    def get_cart_contents(self) -> Dict[Product, int]:
        return self.products.copy()

    def calculate_cart_price(self) -> float:
        if not self.products:
            raise EmptyCartException(
                "Cannot calculate price for an empty cart")

        total_price = sum(product.get_price() * quantity for product,
                          quantity in self.products.items())

        if self.active_promotion is not None:
            discount = self.active_promotion.calculate_discount(self.products)
            return max(0, total_price - discount)

        return total_price

    def activate_promotion(self, promotion: PromotionStrategy) -> None:
        self.active_promotion = promotion

    def is_empty(self) -> bool:
        return len(self.products) == 0

    def clear(self) -> None:
        self.products.clear()
