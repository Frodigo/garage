package com.simple.ecommerce.application.exception;

import com.simple.ecommerce.domain.entity.Product;

/**
 * Exception thrown when trying to add an unavailable product to the shopping cart.
 */
public class ProductUnavailableException extends RuntimeException {

    private final Product product;

    public ProductUnavailableException(Product product) {
        super("Product '" + product.getName() + "' is not available for purchase");
        this.product = product;
    }

    public ProductUnavailableException(String message, Product product) {
        super(message);
        this.product = product;
    }

    /**
     * Gets the unavailable product.
     *
     * @return the product that is unavailable
     */
    public Product getProduct() {
        return product;
    }
}
