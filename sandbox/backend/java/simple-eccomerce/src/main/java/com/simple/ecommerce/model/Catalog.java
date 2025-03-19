package com.simple.ecommerce.model;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Represents the product catalog in the eCommerce system.
 * Business Rules:
 * - Contains all store products
 * - Products filtered by category show only available ones
 * - Products can be sorted alphabetically
 * - Products can be sorted by price (low to high)
 */
public class Catalog {
    private List<Product> products;

    /**
     * Creates an empty catalog.
     */
    public Catalog() {
        this.products = new ArrayList<>();
    }

    /**
     * Adds a product to the catalog.
     *
     * @param product the product to add
     */
    public void addProduct(Product product) {
        if (product == null) {
            throw new IllegalArgumentException("Product cannot be null");
        }
        products.add(product);
    }

    /**
     * Returns all products in the catalog.
     *
     * @return a list of all products
     */
    public List<Product> getAllProducts() {
        return new ArrayList<>(products);
    }

    /**
     * Returns all products sorted alphabetically by name.
     *
     * @return a list of products sorted alphabetically
     */
    public List<Product> getProductsSortedAlphabetically() {
        return products.stream()
                .sorted(Comparator.comparing(Product::getName))
                .collect(Collectors.toList());
    }

    /**
     * Returns available products of the specified category sorted by price (low to high).
     *
     * @param category the category to filter by
     * @return a list of available products in the category sorted by price
     */
    public List<Product> getAvailableProductsByCategory(Category category) {
        if (category == null) {
            throw new IllegalArgumentException("Category cannot be null");
        }
        
        return products.stream()
                .filter(Product::isAvailable)
                .filter(p -> p.getCategory().equals(category))
                .sorted(Comparator.comparing(Product::getPrice))
                .collect(Collectors.toList());
    }
} 