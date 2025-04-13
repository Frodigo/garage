package com.simple.ecommerce.infrastructure.persistence;

import com.simple.ecommerce.application.exception.CategoryNotFoundException;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.domain.repository.ProductRepository;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

/**
 * In-memory implementation of the ProductRepository interface.
 */
public class InMemoryProductRepository implements ProductRepository {

    private final List<Product> products;

    /**
     * Creates an empty in-memory product repository.
     */
    public InMemoryProductRepository() {
        this.products = new ArrayList<>();
    }

    @Override
    public void addProduct(Product product) {
        if (product == null) {
            throw new IllegalArgumentException("Product cannot be null");
        }
        products.add(product);
    }

    @Override
    public List<Product> getAllProducts() {
        return new ArrayList<>(products);
    }

    @Override
    public List<Product> getProductsSortedAlphabetically() {
        return products.stream()
                .sorted(Comparator.comparing(Product::getName))
                .collect(Collectors.toList());
    }

    @Override
    public List<Product> getAvailableProductsByCategory(Category category) {
        if (category == null) {
            throw new CategoryNotFoundException("Category cannot be null");
        }

        return products.stream()
                .filter(Product::isAvailable)
                .filter(p -> p.getCategory().equals(category))
                .sorted(Comparator.comparing(Product::getPrice))
                .collect(Collectors.toList());
    }
}
