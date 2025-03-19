package com.simple.ecommerce.application.exception;

/**
 * Exception thrown when an invalid promotion is applied or when there's an issue with a promotion.
 */
public class InvalidPromotionException extends RuntimeException {
    
    public InvalidPromotionException(String message) {
        super(message);
    }
    
    public InvalidPromotionException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public InvalidPromotionException(String promotionCode, String reason) {
        super("Invalid promotion code '" + promotionCode + "': " + reason);
    }
} 