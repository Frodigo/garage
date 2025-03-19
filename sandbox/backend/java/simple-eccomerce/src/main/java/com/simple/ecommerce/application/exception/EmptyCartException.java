package com.simple.ecommerce.application.exception;

/**
 * Exception thrown when trying to perform an operation on an empty shopping cart.
 */
public class EmptyCartException extends RuntimeException {
    
    public EmptyCartException() {
        super("Operation cannot be performed on an empty shopping cart");
    }
    
    public EmptyCartException(String message) {
        super(message);
    }
    
    public EmptyCartException(String message, Throwable cause) {
        super(message, cause);
    }
} 