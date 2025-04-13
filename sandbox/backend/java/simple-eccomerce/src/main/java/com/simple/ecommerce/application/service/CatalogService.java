package com.simple.ecommerce.application.service;

import com.simple.ecommerce.application.exception.CategoryNotFoundException;
import com.simple.ecommerce.application.exception.ProductNotFoundException;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.domain.repository.ProductRepository;

import java.util.List;
import java.util.Optional;

/**
 * Service for catalog-related operations.
 */
public class CatalogService {

    private final ProductRepository productRepository;

    /**
     * Creates a catalog service with the specified repository.
     *
     * @param productRepository the product repository to use
     * @throws IllegalArgumentException if the repository is null
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
     * @throws IllegalArgumentException if the product is null
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
     * @throws CategoryNotFoundException if the category is null
     */
    public List<Product> getAvailableProductsByCategory(Category category) {
        if (category == null) {
            throw new CategoryNotFoundException("Category cannot be null");
        }
        return productRepository.getAvailableProductsByCategory(category);
    }

    /**
     * Finds a product by its name.
     *
     * @param name the name of the product to find
     * @return the product with the given name
     * @throws ProductNotFoundException if no product with the given name exists
     */
    public Product findProductByName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Product name cannot be null or empty");
        }

        Optional<Product> product = getAllProducts().stream()
                .filter(p -> p.getName().equals(name))
                .findFirst();

        return product.orElseThrow(() ->
            new ProductNotFoundException(name, "Please check the product name and try again."));
    }
}
