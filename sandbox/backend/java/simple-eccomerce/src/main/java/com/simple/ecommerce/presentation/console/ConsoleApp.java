package com.simple.ecommerce.presentation.console;

import com.simple.ecommerce.application.exception.CategoryNotFoundException;
import com.simple.ecommerce.application.exception.EmptyCartException;
import com.simple.ecommerce.application.exception.InvalidPromotionException;
import com.simple.ecommerce.application.exception.ProductNotFoundException;
import com.simple.ecommerce.application.exception.ProductUnavailableException;
import com.simple.ecommerce.application.service.CatalogService;
import com.simple.ecommerce.application.service.ShoppingCartService;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.domain.repository.ProductRepository;
import com.simple.ecommerce.infrastructure.persistence.InMemoryProductRepository;
import com.simple.ecommerce.infrastructure.promotion.CheapestProductPromotion;
import com.simple.ecommerce.infrastructure.promotion.PercentagePromotion;
import com.simple.ecommerce.infrastructure.promotion.SecondProductHalfPricePromotion;

import java.util.List;
import java.util.Map;

/**
 * Console application for the eCommerce system.
 */
public class ConsoleApp {
    public static void main(String[] args) {
        System.out.println("Welcome to Simple eCommerce System");
        System.out.println("==================================\n");
        
        // Initialize repositories and services
        ProductRepository productRepository = new InMemoryProductRepository();
        CatalogService catalogService = new CatalogService(productRepository);
        ShoppingCartService cartService = new ShoppingCartService();
        
        // Initialize catalog with sample data
        initializeCatalog(catalogService);
        
        // Display all products alphabetically
        System.out.println("All products (sorted alphabetically):");
        List<Product> sortedProducts = catalogService.getProductsSortedAlphabetically();
        sortedProducts.forEach(product -> 
            System.out.println(" - " + product.getName() + " ($" + product.getPrice() + ")"));
        
        // Display products by category
        Category electronics = new Category("Electronics");
        System.out.println("\nElectronics products (sorted by price):");
        List<Product> electronicProducts = catalogService.getAvailableProductsByCategory(electronics);
        electronicProducts.forEach(product -> 
            System.out.println(" - " + product.getName() + " ($" + product.getPrice() + ")"));
        
        // Demonstrate shopping cart
        demonstrateShoppingCart(sortedProducts, cartService);
        
        // Demonstrate promotions
        demonstratePromotions(cartService);
        
        // Demonstrate exception handling
        System.out.println("\n=== Exception Handling Demonstration ===");
        demonstrateExceptionHandling(catalogService, cartService);
    }
    
    /**
     * Initializes the catalog with sample products.
     *
     * @param catalogService the catalog service to use
     */
    private static void initializeCatalog(CatalogService catalogService) {
        // Create categories
        Category electronics = new Category("Electronics");
        Category books = new Category("Books");
        Category clothing = new Category("Clothing");
        
        // Electronics
        catalogService.addProduct(new Product("Laptop", 1200.0, electronics));
        catalogService.addProduct(new Product("Smartphone", 800.0, electronics));
        catalogService.addProduct(new Product("Headphones", 150.0, electronics));
        catalogService.addProduct(new Product("Tablet", 500.0, electronics));
        catalogService.addProduct(new Product("Smart Watch", 250.0, electronics));
        
        // Books
        catalogService.addProduct(new Product("Java Programming", 45.0, books));
        catalogService.addProduct(new Product("Clean Code", 35.0, books));
        catalogService.addProduct(new Product("Design Patterns", 40.0, books));
        catalogService.addProduct(new Product("Algorithms", 50.0, books));
        
        // Clothing
        catalogService.addProduct(new Product("T-Shirt", 25.0, clothing));
        catalogService.addProduct(new Product("Jeans", 60.0, clothing));
        catalogService.addProduct(new Product("Hoodie", 45.0, clothing));
        
        // Mark one product as unavailable
        Product unavailableProduct = new Product("Out of Stock Item", 99.0, electronics);
        unavailableProduct.setAvailable(false);
        catalogService.addProduct(unavailableProduct);
    }
    
    /**
     * Demonstrates adding products to the shopping cart.
     *
     * @param products the available products
     * @param cartService the shopping cart service to use
     */
    private static void demonstrateShoppingCart(List<Product> products, ShoppingCartService cartService) {
        // Find products by name
        Product laptop = findProductByName(products, "Laptop");
        Product smartphone = findProductByName(products, "Smartphone");
        Product headphones = findProductByName(products, "Headphones");
        
        // Add products to cart
        cartService.addProduct(laptop);
        cartService.addProduct(smartphone);
        cartService.addProduct(headphones);
        cartService.addProduct(headphones); // Adding a second pair of headphones
        
        // Display cart contents
        System.out.println("\nShopping Cart Contents:");
        Map<Product, Integer> cartContents = cartService.getCartContents();
        cartContents.forEach((product, quantity) -> 
            System.out.println(" - " + product.getName() + " x" + quantity + 
                              " ($" + product.getPrice() + " each)"));
        
        // Calculate and display total price without promotions
        System.out.println("\nTotal Price: $" + String.format("%.2f", cartService.calculateCartPrice()));
    }
    
    /**
     * Demonstrates applying different promotions to the shopping cart.
     *
     * @param cartService the shopping cart service to use
     */
    private static void demonstratePromotions(ShoppingCartService cartService) {
        // 10% off everything promotion
        PercentagePromotion tenPercentOff = new PercentagePromotion("10PERCENTOFF");
        cartService.activatePromotion(tenPercentOff);
        System.out.println("\nWith 10% off promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cartService.calculateCartPrice()));
        
        // Every 3rd item costs 1 PLN promotion
        CheapestProductPromotion everyThirdCheapPromotion = new CheapestProductPromotion("EVERY3RD1PLN");
        cartService.activatePromotion(everyThirdCheapPromotion);
        System.out.println("\nWith every 3rd item for 1 PLN promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cartService.calculateCartPrice()));
        
        // Second item half price promotion
        SecondProductHalfPricePromotion secondHalfPricePromotion = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        cartService.activatePromotion(secondHalfPricePromotion);
        System.out.println("\nWith second item half price promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cartService.calculateCartPrice()));
    }
    
    /**
     * Demonstrates exception handling for various scenarios.
     *
     * @param catalogService the catalog service to use
     * @param cartService the shopping cart service to use
     */
    private static void demonstrateExceptionHandling(CatalogService catalogService, ShoppingCartService cartService) {
        // 1. ProductNotFoundException
        System.out.println("\n1. ProductNotFoundException handling:");
        try {
            System.out.println("  Trying to find non-existent product 'Gaming Console'...");
            Product nonExistentProduct = catalogService.findProductByName("Gaming Console");
            System.out.println("  Found product: " + nonExistentProduct.getName());
        } catch (ProductNotFoundException e) {
            System.out.println("  Error: " + e.getMessage());
        }
        
        // 2. ProductUnavailableException
        System.out.println("\n2. ProductUnavailableException handling:");
        try {
            System.out.println("  Trying to add unavailable product to cart...");
            Product unavailableProduct = findProductByName(catalogService.getAllProducts(), "Out of Stock Item");
            cartService.addProduct(unavailableProduct);
            System.out.println("  Product added successfully");
        } catch (ProductUnavailableException e) {
            System.out.println("  Error: " + e.getMessage());
            System.out.println("  Unavailable product: " + e.getProduct().getName());
        }
        
        // 3. CategoryNotFoundException
        System.out.println("\n3. CategoryNotFoundException handling:");
        try {
            System.out.println("  Trying to get products with null category...");
            catalogService.getAvailableProductsByCategory(null);
            System.out.println("  Products retrieved successfully");
        } catch (CategoryNotFoundException e) {
            System.out.println("  Error: " + e.getMessage());
        }
        
        // 4. InvalidPromotionException
        System.out.println("\n4. InvalidPromotionException handling:");
        try {
            System.out.println("  Trying to create promotion with invalid discount percentage...");
            PercentagePromotion invalidPromotion = new PercentagePromotion("INVALID_PROMO", 110.0);
            System.out.println("  Promotion created successfully: " + invalidPromotion.getPromotionCode());
        } catch (InvalidPromotionException e) {
            System.out.println("  Error: " + e.getMessage());
        }
        
        // 5. EmptyCartException
        System.out.println("\n5. EmptyCartException handling:");
        try {
            System.out.println("  Trying to calculate price with empty cart...");
            // Create a new cart that is empty
            ShoppingCartService emptyCart = new ShoppingCartService();
            emptyCart.calculateCartPrice();
            System.out.println("  Price calculated successfully");
        } catch (EmptyCartException e) {
            System.out.println("  Error: " + e.getMessage());
        }
        
        // 6. Demonstrate proper exception recovery
        System.out.println("\n6. Exception recovery demonstration:");
        ShoppingCartService recoveryCart = new ShoppingCartService();
        
        // Try to calculate price with empty cart
        try {
            System.out.println("  Trying to calculate price with empty cart...");
            recoveryCart.calculateCartPrice();
        } catch (EmptyCartException e) {
            System.out.println("  Error: " + e.getMessage());
            System.out.println("  Recovering by adding a product to cart...");
            
            // Add a product and try again
            Product laptop = findProductByName(catalogService.getAllProducts(), "Laptop");
            recoveryCart.addProduct(laptop);
            
            try {
                double price = recoveryCart.calculateCartPrice();
                System.out.println("  Recovery successful! Cart price: $" + String.format("%.2f", price));
            } catch (Exception recoveryException) {
                System.out.println("  Recovery failed: " + recoveryException.getMessage());
            }
        }
        
        System.out.println("\nException handling demonstration completed.");
    }
    
    /**
     * Helper method to find a product by name from a list of products.
     *
     * @param products the list of products to search in
     * @param name the name of the product to find
     * @return the found product or null if not found
     */
    private static Product findProductByName(List<Product> products, String name) {
        return products.stream()
                .filter(p -> p.getName().equals(name))
                .findFirst()
                .orElse(null);
    }
} 