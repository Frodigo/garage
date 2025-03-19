package com.simple.ecommerce;

import java.util.List;
import java.util.Map;

import com.simple.ecommerce.model.Catalog;
import com.simple.ecommerce.model.Category;
import com.simple.ecommerce.model.Product;
import com.simple.ecommerce.model.ShoppingCart;
import com.simple.ecommerce.promotion.CheapestProductPromotion;
import com.simple.ecommerce.promotion.PercentagePromotion;
import com.simple.ecommerce.promotion.SecondProductHalfPricePromotion;

/**
 * Main application class for the simple eCommerce system.
 */
public class App {
    public static void main(String[] args) {
        System.out.println("Welcome to Simple eCommerce System");
        System.out.println("==================================\n");
        
        // Create categories
        Category electronics = new Category("Electronics");
        Category books = new Category("Books");
        Category clothing = new Category("Clothing");
        
        // Initialize catalog with sample products
        Catalog catalog = createSampleCatalog(electronics, books, clothing);
        
        // Display all products alphabetically
        System.out.println("All products (sorted alphabetically):");
        List<Product> sortedProducts = catalog.getProductsSortedAlphabetically();
        sortedProducts.forEach(product -> 
            System.out.println(" - " + product.getName() + " ($" + product.getPrice() + ")"));
        
        System.out.println("\nElectronics products (sorted by price):");
        List<Product> electronicProducts = catalog.getAvailableProductsByCategory(electronics);
        electronicProducts.forEach(product -> 
            System.out.println(" - " + product.getName() + " ($" + product.getPrice() + ")"));
        
        // Shopping cart demonstration
        ShoppingCart cart = new ShoppingCart();
        Product laptop = sortedProducts.stream()
                .filter(p -> p.getName().equals("Laptop"))
                .findFirst().orElse(null);
        Product smartphone = sortedProducts.stream()
                .filter(p -> p.getName().equals("Smartphone"))
                .findFirst().orElse(null);
        Product headphones = sortedProducts.stream()
                .filter(p -> p.getName().equals("Headphones"))
                .findFirst().orElse(null);
        
        // Add products to cart
        cart.addProduct(laptop);
        cart.addProduct(smartphone);
        cart.addProduct(headphones);
        cart.addProduct(headphones); // Adding a second pair of headphones
        
        // Display cart contents
        System.out.println("\nShopping Cart Contents:");
        Map<Product, Integer> cartContents = cart.getCartContents();
        cartContents.forEach((product, quantity) -> 
            System.out.println(" - " + product.getName() + " x" + quantity + 
                              " ($" + product.getPrice() + " each)"));
        
        // Calculate and display total price without promotions
        System.out.println("\nTotal Price: $" + String.format("%.2f", cart.calculateCartPrice()));
        
        // Apply different promotions and show the discounted prices
        demonstratePromotions(cart);
    }
    
    /**
     * Creates a sample catalog with predefined products.
     */
    private static Catalog createSampleCatalog(Category electronics, Category books, Category clothing) {
        Catalog catalog = new Catalog();
        
        // Electronics
        catalog.addProduct(new Product("Laptop", 1200.0, electronics));
        catalog.addProduct(new Product("Smartphone", 800.0, electronics));
        catalog.addProduct(new Product("Headphones", 150.0, electronics));
        catalog.addProduct(new Product("Tablet", 500.0, electronics));
        catalog.addProduct(new Product("Smart Watch", 250.0, electronics));
        
        // Books
        catalog.addProduct(new Product("Java Programming", 45.0, books));
        catalog.addProduct(new Product("Clean Code", 35.0, books));
        catalog.addProduct(new Product("Design Patterns", 40.0, books));
        catalog.addProduct(new Product("Algorithms", 50.0, books));
        
        // Clothing
        catalog.addProduct(new Product("T-Shirt", 25.0, clothing));
        catalog.addProduct(new Product("Jeans", 60.0, clothing));
        catalog.addProduct(new Product("Hoodie", 45.0, clothing));
        
        // Mark one product as unavailable
        Product unavailableProduct = new Product("Out of Stock Item", 99.0, electronics);
        unavailableProduct.setAvailable(false);
        catalog.addProduct(unavailableProduct);
        
        return catalog;
    }
    
    /**
     * Demonstrates different promotions on the shopping cart.
     */
    private static void demonstratePromotions(ShoppingCart cart) {
        // 10% off everything promotion
        PercentagePromotion tenPercentOff = new PercentagePromotion("10PERCENTOFF");
        cart.activatePromotion(tenPercentOff);
        System.out.println("\nWith 10% off promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cart.calculateCartPrice()));
        
        // Every 3rd item costs 1 PLN promotion
        CheapestProductPromotion everyThirdCheapPromotion = new CheapestProductPromotion("EVERY3RD1PLN");
        cart.activatePromotion(everyThirdCheapPromotion);
        System.out.println("\nWith every 3rd item for 1 PLN promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cart.calculateCartPrice()));
        
        // Second item half price promotion
        SecondProductHalfPricePromotion secondHalfPricePromotion = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        cart.activatePromotion(secondHalfPricePromotion);
        System.out.println("\nWith second item half price promotion:");
        System.out.println("Total Price: $" + String.format("%.2f", cart.calculateCartPrice()));
    }
}
