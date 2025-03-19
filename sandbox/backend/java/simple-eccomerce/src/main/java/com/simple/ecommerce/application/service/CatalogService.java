package com.simple.ecommerce.application.service;

import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.domain.repository.ProductRepository;

import java.util.List;

/**
 * Service for catalog-related operations.
 */
public class CatalogService {
    
    private final ProductRepository productRepository;
    
    /**
     * Creates a catalog service with the specified repository.
     *
     * @param productRepository the product repository to use
     */
    public CatalogService(ProductRepository productRepository) {
        if (productRepository == null) {
            throw new IllegalArgumentException("Product repository cannot be null");
        }
        this.productRepository = productRepository;
    }
    
    /**
     * Adds a product to the catalog.
     *
     * @param product the product to add
     */
    public void addProduct(Product product) {
        productRepository.addProduct(product);
    }
    
    /**
     * Returns all products in the catalog.
     *
     * @return a list of all products
     */
    public List<Product> getAllProducts() {
        return productRepository.getAllProducts();
    }
    
    /**
     * Returns all products sorted alphabetically by name.
     *
     * @return a list of products sorted alphabetically
     */
    public List<Product> getProductsSortedAlphabetically() {
        return productRepository.getProductsSortedAlphabetically();
    }
    
    /**
     * Returns available products of the specified category sorted by price (low to high).
     *
     * @param category the category to filter by
     * @return a list of available products in the category sorted by price
     */
    public List<Product> getAvailableProductsByCategory(Category category) {
        return productRepository.getAvailableProductsByCategory(category);
    }
} 