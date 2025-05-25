# p911 - Simple eCommerce Backend

A console-based eCommerce application backend written in Python, following Clean Architecture principles.

## Project Overview

This project demonstrates a simple yet complete implementation of an eCommerce system with the following features:

- Product and category management
- Shopping cart functionality
- Various promotion strategies
- Custom exception handling
- Clean Architecture implementation

## Architecture

The application follows Clean Architecture with the following layers:

### Domain Layer

- Core business entities like `Product` and `Category`
- Repository interfaces

### Application Layer

- Business services: `CatalogService`, `ShoppingCartService`
- Custom exceptions for better error handling
- Port interfaces for external dependencies

### Infrastructure Layer

- Repository implementations (e.g., `InMemoryProductRepository`)
- Promotion strategy implementations

### Presentation Layer

- Console-based user interface (`ConsoleApp`)

## Solution Design

The following diagrams represent the system architecture using the C4 Model approach:

### Context Diagram (Level 1)

```mermaid
C4Context
    title System Context Diagram for eCommerce System

    Person(customer, "Customer", "A user of the eCommerce system")
    System(ecommerceSystem, "eCommerce System", "Allows customers to browse products, manage shopping cart and apply promotions")

    Rel(customer, ecommerceSystem, "Uses")
```

### Container Diagram (Level 2)

```mermaid
C4Container
    title Container Diagram for eCommerce System

    Person(customer, "Customer", "A user of the eCommerce system")

    System_Boundary(ecommerceSystem, "eCommerce System") {
        Container(consoleApp, "Console Application", "Python", "Provides user interface via console commands")
        ContainerDb(inMemoryDatabase, "In-Memory Database", "In-Memory", "Stores product information")
    }

    Rel(customer, consoleApp, "Interacts with")
    Rel(consoleApp, inMemoryDatabase, "Reads from and writes to")
```

### Component Diagram (Level 3)

```mermaid
C4Component
    title Component Diagram for eCommerce System Business Logic

    Container_Boundary(businessLogic, "Business Logic") {
        Component(catalogService, "Catalog Service", "Python", "Provides product catalog functionality")
        Component(shoppingCartService, "Shopping Cart Service", "Python", "Manages shopping cart operations")
        Component(promotionStrategies, "Promotion Strategies", "Python", "Implements various discount strategies")
    }

    Container(productRepository, "Product Repository", "In-Memory", "Stores product information")
    Container(consoleApp, "Console Application", "Python", "Provides UI via console")

    Rel(consoleApp, catalogService, "Uses")
    Rel(consoleApp, shoppingCartService, "Uses")
    Rel(shoppingCartService, promotionStrategies, "Applies")
    Rel(catalogService, productRepository, "Reads from")
```

### Class Diagram (Level 4)

```mermaid
classDiagram
    %% Domain Layer
    class Product {
        -str name
        -float price
        -bool available
        -Category category
        +is_available()
        +get_price()
        +get_name()
        +get_category()
    }
    class Category {
        -str name
        +get_name()
    }

    %% Application Layer
    class CatalogService {
        +get_all_products()
        +get_products_sorted_alphabetically()
        +get_available_products_by_category()
        +find_product_by_name()
    }
    class ShoppingCartService {
        +add_product()
        +remove_product()
        +calculate_cart_price()
        +activate_promotion()
    }
    class PromotionStrategy {
        <<interface>>
        +calculate_discount()
        +get_promotion_code()
    }

    %% Infrastructure Layer
    class InMemoryProductRepository {
        +add_product()
        +get_all_products()
        +get_products_sorted_alphabetically()
        +get_available_products_by_category()
    }
    class PercentagePromotion {
        +calculate_discount()
    }
    class SecondProductHalfPricePromotion {
        +calculate_discount()
    }
    class CheapestProductPromotion {
        +calculate_discount()
    }

    %% Relationships
    Product --> Category
    CatalogService --> InMemoryProductRepository
    ShoppingCartService --> PromotionStrategy
    PercentagePromotion ..|> PromotionStrategy
    SecondProductHalfPricePromotion ..|> PromotionStrategy
    CheapestProductPromotion ..|> PromotionStrategy
    InMemoryProductRepository --> Product
```

## Features

### Product Management

- Create and manage products with name, price, and category
- Mark products as available/unavailable
- Sort products alphabetically or by price
- Filter products by category

### Shopping Cart

- Add and remove products from cart
- Calculate cart total price
- Show detailed cart contents

### Promotion System

- Percentage-based discounts
- "Second item half price" promotions
- "Cheapest product discount" promotions
- Flexible promotion strategy pattern

### Exception Handling

- Custom exceptions for different error scenarios:
  - `ProductNotFoundException`: When a product doesn't exist
  - `ProductUnavailableException`: When trying to purchase unavailable products
  - `EmptyCartException`: When operations are performed on empty carts
  - `CategoryNotFoundException`: When a category doesn't exist
  - `InvalidPromotionException`: When promotion parameters are incorrect

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.8 or higher

You can check your installation with:

```bash
python --version
```

## Running the Application

To run the application:

```bash
python app.py
```

Or using the module approach:

```bash
python -m app
```

The demonstration will show:

1. Products sorted alphabetically
2. Products filtered by category
3. Shopping cart functionality
4. Different promotion types applied to a cart
5. Exception handling examples
