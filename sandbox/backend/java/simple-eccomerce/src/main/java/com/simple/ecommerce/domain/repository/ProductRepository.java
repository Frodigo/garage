package com.simple.ecommerce.domain.repository;

import com.simple.ecommerce.application.exception.CategoryNotFoundException;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;

import java.util.List;

/**
 * Repository interface for product operations.
 */
public interface ProductRepository {

    /**
     * Adds a product to the repository.
     *
     * @param product the product to add
     * @throws IllegalArgumentException if product is null
     */
    void addProduct(Product product);

    /**
     * Returns all products in the repository.
     *
     * @return a list of all products
     */
    List<Product> getAllProducts();

    /**
     * Returns all products sorted alphabetically by name.
     *
     * @return a list of products sorted alphabetically
     */
    List<Product> getProductsSortedAlphabetically();

    /**
     * Returns available products of the specified category sorted by price (low to high).
     *
     * @param category the category to filter by
     * @return a list of available products in the category sorted by price
     * @throws CategoryNotFoundException if category is null
     */
    List<Product> getAvailableProductsByCategory(Category category);
}
