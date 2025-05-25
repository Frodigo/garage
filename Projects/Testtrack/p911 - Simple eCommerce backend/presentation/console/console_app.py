from typing import List, Optional
from application import CategoryNotFoundException, EmptyCartException, InvalidPromotionException, ProductNotFoundException, ProductUnavailableException, CatalogService, ShoppingCartService
from domain import Category, Product
from infrastructure import InMemoryProductRepository, CheapestProductPromotion, PercentagePromotion, SecondProductHalfPricePromotion


def main():
    print("Welcome to Simple eCommerce System")
    print("==================================\n")

    product_repository = InMemoryProductRepository()
    catalog_service = CatalogService(product_repository)
    cart_service = ShoppingCartService()

    initialize_catalog(catalog_service)

    print("All products (sorted alphabetically):")
    sorted_products = catalog_service.get_products_sorted_alphabetically()
    for product in sorted_products:
        print(f" - {product.get_name()} (${product.get_price()})")

    electronics = Category("Electronics")
    print("\nElectronics products (sorted by price):")
    electronic_products = catalog_service.get_available_products_by_category(
        electronics)
    for product in electronic_products:
        print(f" - {product.get_name()} (${product.get_price()})")

    demonstrate_shopping_cart(sorted_products, cart_service)
    demonstrate_promotions(cart_service)

    print("\n=== Exception Handling Demonstration ===")
    demonstrate_exception_handling(catalog_service, cart_service)


def initialize_catalog(catalog_service: CatalogService) -> None:
    electronics = Category("Electronics")
    books = Category("Books")
    clothing = Category("Clothing")

    catalog_service.add_product(Product("Laptop", 1200.0, electronics))
    catalog_service.add_product(Product("Smartphone", 800.0, electronics))
    catalog_service.add_product(Product("Headphones", 150.0, electronics))
    catalog_service.add_product(Product("Tablet", 500.0, electronics))
    catalog_service.add_product(Product("Smart Watch", 250.0, electronics))

    catalog_service.add_product(Product("Java Programming", 45.0, books))
    catalog_service.add_product(Product("Clean Code", 35.0, books))
    catalog_service.add_product(Product("Design Patterns", 40.0, books))
    catalog_service.add_product(Product("Algorithms", 50.0, books))

    catalog_service.add_product(Product("T-Shirt", 25.0, clothing))
    catalog_service.add_product(Product("Jeans", 60.0, clothing))
    catalog_service.add_product(Product("Hoodie", 45.0, clothing))

    unavailable_product = Product("Out of Stock Item", 99.0, electronics)
    unavailable_product.set_available(False)
    catalog_service.add_product(unavailable_product)


def demonstrate_shopping_cart(products: List[Product], cart_service: ShoppingCartService) -> None:
    laptop = find_product_by_name(products, "Laptop")
    smartphone = find_product_by_name(products, "Smartphone")
    headphones = find_product_by_name(products, "Headphones")

    cart_service.add_product(laptop)
    cart_service.add_product(smartphone)
    cart_service.add_product(headphones)
    cart_service.add_product(headphones)

    print("\nShopping Cart Contents:")
    cart_contents = cart_service.get_cart_contents()
    for product, quantity in cart_contents.items():
        print(f" - {product.get_name()} x{quantity} (${product.get_price()} each)")

    print(f"\nTotal Price: ${cart_service.calculate_cart_price():.2f}")


def demonstrate_promotions(cart_service: ShoppingCartService) -> None:
    ten_percent_off = PercentagePromotion("10PERCENTOFF")
    cart_service.activate_promotion(ten_percent_off)
    print("\nWith 10% off promotion:")
    print(f"Total Price: ${cart_service.calculate_cart_price():.2f}")

    every_third_cheap_promotion = CheapestProductPromotion("EVERY3RD1PLN")
    cart_service.activate_promotion(every_third_cheap_promotion)
    print("\nWith every 3rd item for 1 PLN promotion:")
    print(f"Total Price: ${cart_service.calculate_cart_price():.2f}")

    second_half_price_promotion = SecondProductHalfPricePromotion(
        "SECONDHALFPRICE")
    cart_service.activate_promotion(second_half_price_promotion)
    print("\nWith second item half price promotion:")
    print(f"Total Price: ${cart_service.calculate_cart_price():.2f}")


def demonstrate_exception_handling(catalog_service: CatalogService, cart_service: ShoppingCartService) -> None:
    print("\n1. ProductNotFoundException handling:")
    try:
        print("  Trying to find non-existent product 'Gaming Console'...")
        non_existent_product = catalog_service.find_product_by_name(
            "Gaming Console")
        print(f"  Found product: {non_existent_product.get_name()}")
    except ProductNotFoundException as e:
        print(f"  Error: {e}")

    print("\n2. ProductUnavailableException handling:")
    try:
        print("  Trying to add unavailable product to cart...")
        unavailable_product = find_product_by_name(
            catalog_service.get_all_products(), "Out of Stock Item")
        cart_service.add_product(unavailable_product)
        print("  Product added successfully")
    except ProductUnavailableException as e:
        print(f"  Error: {e}")
        print(f"  Unavailable product: {e.get_product().get_name()}")

    print("\n3. CategoryNotFoundException handling:")
    try:
        print("  Trying to get products with null category...")
        catalog_service.get_available_products_by_category(None)
        print("  Products retrieved successfully")
    except CategoryNotFoundException as e:
        print(f"  Error: {e}")

    print("\n4. InvalidPromotionException handling:")
    try:
        print("  Trying to create promotion with invalid discount percentage...")
        invalid_promotion = PercentagePromotion("INVALID_PROMO", 110.0)
        print(
            f"  Promotion created successfully: {invalid_promotion.get_promotion_code()}")
    except InvalidPromotionException as e:
        print(f"  Error: {e}")

    print("\n5. EmptyCartException handling:")
    try:
        print("  Trying to calculate price with empty cart...")
        empty_cart = ShoppingCartService()
        empty_cart.calculate_cart_price()
        print("  Price calculated successfully")
    except EmptyCartException as e:
        print(f"  Error: {e}")

    print("\n6. Exception recovery demonstration:")
    recovery_cart = ShoppingCartService()

    try:
        print("  Trying to calculate price with empty cart...")
        recovery_cart.calculate_cart_price()
    except EmptyCartException as e:
        print(f"  Error: {e}")
        print("  Recovering by adding a product to cart...")

        laptop = find_product_by_name(
            catalog_service.get_all_products(), "Laptop")
        recovery_cart.add_product(laptop)

        try:
            price = recovery_cart.calculate_cart_price()
            print(f"  Recovery successful! Cart price: ${price:.2f}")
        except Exception as recovery_exception:
            print(f"  Recovery failed: {recovery_exception}")

    print("\nException handling demonstration completed.")


def find_product_by_name(products: List[Product], name: str) -> Optional[Product]:
    for product in products:
        if product.get_name() == name:
            return product
    return None


if __name__ == "__main__":
    main()
