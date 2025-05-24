from typing import List
from application.exception.category_not_found_exception import CategoryNotFoundException
from application.exception.product_not_found_exception import ProductNotFoundException
from domain import Category
from domain import Product
from domain import ProductRepository


class CatalogService:
    def __init__(self, product_repository: ProductRepository):
        if product_repository is None:
            raise ValueError("Product repository cannot be null")
        else:
            self.product_repository = product_repository

    def add_product(self, product: Product) -> None:
        self.product_repository.add_product(product)

    def get_all_products(self) -> List[Product]:
        return self.product_repository.get_all_products()

    def get_products_sorted_alphabetically(self) -> List[Product]:
        return self.product_repository.get_products_sorted_alphabetically()

    def get_available_products_by_category(self, category: Category) -> List[Product]:
        if category is None:
            raise CategoryNotFoundException("Category cannot be null")
        return self.product_repository.get_available_products_by_category(category)

    def find_product_by_name(self, name: str) -> Product:
        if not name or name.strip() == "":
            raise ValueError("Product name cannot be null or empty")

        for product in self.get_all_products():
            if product.get_name() == name:
                return product

        raise ProductNotFoundException(
            name, "Please check the product name and try again.")
