from typing import List
from application import CategoryNotFoundException
from domain import Category, Product, ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: List[Product] = []

    def add_product(self, product: Product) -> None:
        if product is None:
            raise ValueError("Product cannot be null")
        else:
            self.products.append(product)

    def get_all_products(self) -> List[Product]:
        return self.products.copy()

    def get_products_sorted_alphabetically(self) -> List[Product]:
        return sorted(self.products, key=lambda p: p.get_name())

    def get_available_products_by_category(self, category: Category) -> List[Product]:
        if category is None:
            raise CategoryNotFoundException("Category cannot be null")

        available_products = [
            p for p in self.products if p.is_available() and p.get_category() == category]
        return sorted(available_products, key=lambda p: p.get_price())
