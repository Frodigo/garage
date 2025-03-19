Create a console backend for a simple eCommerce platform enabling customers to shop online.

## Tasks
- Implement Product class
- Design and implement Product Catalog
- Design and implement Shopping Cart
- Add Promotion functionality
- Create a simple class diagram
- Implement unit tests

## Acceptance Criteria

### Product Class
- [ ] Implement Product class with attributes: name, price, category
- [ ] Functionality to mark products as available/unavailable

### Product Catalog
- [ ] Store all products available for purchase
- [ ] Auto-populate catalog with predefined products at application startup
- [ ] Ability to retrieve and display names and prices of all products (alphabetical sorting)
- [ ] Ability to filter products by category (sorting from cheapest, filtering unavailable products)

### Shopping Cart
- [ ] Ability to add products to cart (including multiple instances of the same product)
- [ ] Ability to remove products from cart
- [ ] Display cart contents (product names and quantities)
- [ ] Calculate and display the total price of all products in the cart

### Promotions
- [ ] Add promotions to shopping cart using discount codes
- [ ] Implement "10% off all products in cart" promotion
- [ ] Implement "when buying 3 products, the cheapest one costs 1 PLN" promotion
- [ ] Implement "when buying 2 identical products, the second one is half price" promotion

### Documentation and Testing
- [ ] Create a simple class diagram showing relationships between classes
- [ ] Implement unit tests using JUnit5 and the given-when-then technique


---

## Diagram 
```mermaid
classDiagram

%% Core Business Entities

  

class Product {

%% Attributes

-String name

-double price

-Category category

-boolean available

%% Methods

+getName() String

+getPrice() double

+getCategory() Category

+isAvailable() boolean

+setAvailable(boolean available) void

%% Business Rules

BR: Must have name, price and category

BR: Can be marked available or unavailable

}

class Category {

%% Attributes

-String name

%% Methods

+getName() String

%% Business Rules

BR: Each product has exactly one category

}

class Catalog {

%% Attributes

-List~Product~ products

%% Methods

+addProduct(Product product) void

+getAllProducts() List~Product~

+getProductsSortedAlphabetically() List~Product~

+getAvailableProductsByCategory(Category category) List~Product~

%% Business Rules

BR: Contains all store products

BR: Products filtered by category show only available ones

BR: Products can be sorted alphabetically

BR: Products can be sorted by price (low to high)

}

class ShoppingCart {

%% Attributes

-Map~Product, Integer~ products

-Promotion activePromotion

%% Methods

+addProduct(Product product) void

+removeProduct(Product product) void

+getCartContents() Map~Product, Integer~

+calculateCartPrice() double

+activatePromotion(Promotion promotion) void

%% Business Rules

BR: Initially empty

BR: Can have multiple units of same product

BR: Total price = sum of product prices with applied promotion

BR: Only one active promotion at a time

BR: New promotion overrides previous one

}

%% Interface for Promotion Strategy Pattern

class Promotion {

<<interface>>

%% Methods

+calculateDiscount(Map~Product, Integer~ products) double

+getPromotionCode() String

%% Business Rules

BR: Only one promotion active at a time

BR: Applied during price calculation

}

%% Concrete Promotion Implementation Classes

class PercentagePromotion {

%% Attributes

-String promotionCode

-double discountPercentage

%% Methods

+calculateDiscount(Map~Product, Integer~ products) double

+getPromotionCode() String

%% Business Rules

BR: Applies 10% discount to entire cart

}

class CheapestProductPromotion {

%% Attributes

-String promotionCode

-double specialPrice

-int productsRequired

%% Methods

+calculateDiscount(Map~Product, Integer~ products) double

+getPromotionCode() String

%% Business Rules

BR: Every third product costs 1 PLN

BR: Applied to cheapest products first

}

class SecondProductHalfPricePromotion {

%% Attributes

-String promotionCode

%% Methods

+calculateDiscount(Map~Product, Integer~ products) double

+getPromotionCode() String

%% Business Rules

BR: Second identical product costs 50% of original price

BR: Applied for each product type separately

}

%% Relationships

Product --> Category : has

Catalog o-- "many" Product : contains

ShoppingCart o-- "many" Product : contains

ShoppingCart --> Promotion : uses

Promotion <|.. PercentagePromotion : implements

Promotion <|.. CheapestProductPromotion : implements

Promotion <|.. SecondProductHalfPricePromotion : implements
```

