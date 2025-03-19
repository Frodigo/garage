package com.simple.ecommerce.promotion;

import java.util.Map;

import com.simple.ecommerce.model.Product;

/**
 * Applies a percentage discount to the entire cart.
 * Business Rules:
 * - Applies 10% discount to entire cart
 */
public class PercentagePromotion implements Promotion {
    private static final double DEFAULT_DISCOUNT_PERCENTAGE = 10.0;
    
    private String promotionCode;
    private double discountPercentage;

    /**
     * Creates a new percentage promotion with the default 10% discount.
     *
     * @param promotionCode the promotion code
     */
    public PercentagePromotion(String promotionCode) {
        this(promotionCode, DEFAULT_DISCOUNT_PERCENTAGE);
    }

    /**
     * Creates a new percentage promotion with a custom discount percentage.
     *
     * @param promotionCode the promotion code
     * @param discountPercentage the discount percentage (0-100)
     */
    public PercentagePromotion(String promotionCode, double discountPercentage) {
        if (promotionCode == null || promotionCode.trim().isEmpty()) {
            throw new IllegalArgumentException("Promotion code cannot be empty");
        }
        if (discountPercentage < 0 || discountPercentage > 100) {
            throw new IllegalArgumentException("Discount percentage must be between 0 and 100");
        }
        
        this.promotionCode = promotionCode;
        this.discountPercentage = discountPercentage;
    }

    @Override
    public double calculateDiscount(Map<Product, Integer> products) {
        double totalPrice = products.entrySet().stream()
                .mapToDouble(entry -> entry.getKey().getPrice() * entry.getValue())
                .sum();
        
        return totalPrice * (discountPercentage / 100.0);
    }

    @Override
    public String getPromotionCode() {
        return promotionCode;
    }
} 