package com.simple.ecommerce.application.port;

import com.simple.ecommerce.domain.entity.Product;

import java.util.Map;

/**
 * Interface for different types of promotions.
 * Business Rules:
 * - Only one promotion active at a time
 * - Applied during price calculation
 */
public interface PromotionStrategy {
    
    /**
     * Calculates the discount for the items in the shopping cart.
     *
     * @param products a map of products and their quantities in the cart
     * @return the total discount amount
     */
    double calculateDiscount(Map<Product, Integer> products);
    
    /**
     * Returns the promotion code.
     *
     * @return the promotion code
     */
    String getPromotionCode();
} 