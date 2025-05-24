from typing import Optional
from domain import Product


class ProductUnavailableException(Exception):
    def __init__(self, product: Product, message: Optional[str] = None):
        if message is None:
            message = f"Product '{product.get_name()}' is not available for purchase"
        super().__init__(message)
        self._product = product

    def get_product(self) -> Product:
        return self._product
