package com.simple.ecommerce.application.exception;

/**
 * Exception thrown when a category cannot be found.
 */
public class CategoryNotFoundException extends RuntimeException {
    
    public CategoryNotFoundException(String message) {
        super(message);
    }
    
    public CategoryNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public CategoryNotFoundException(Long categoryId) {
        super("Category with ID " + categoryId + " not found");
    }
    
    /**
     * Creates a new exception for a category not found by name.
     *
     * @param categoryName the name of the category that wasn't found
     * @param exactMatch whether the search was for an exact match
     * @return the exception
     */
    public static CategoryNotFoundException forName(String categoryName, boolean exactMatch) {
        String message = "Category with name '" + categoryName + "' not found";
        if (exactMatch) {
            message += " (exact match)";
        }
        return new CategoryNotFoundException(message);
    }
} 