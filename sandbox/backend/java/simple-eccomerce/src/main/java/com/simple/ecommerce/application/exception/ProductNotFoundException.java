package com.simple.ecommerce.application.exception;

/**
 * Exception thrown when a product cannot be found.
 */
public class ProductNotFoundException extends RuntimeException {
    
    public ProductNotFoundException(String message) {
        super(message);
    }
    
    public ProductNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public ProductNotFoundException(Long productId) {
        super("Product with ID " + productId + " not found");
    }
    
    public ProductNotFoundException(String productName, String additionalInfo) {
        super("Product with name '" + productName + "' not found. " + additionalInfo);
    }
} 