package com.simple.ecommerce.promotion;

import java.util.Map;

import com.simple.ecommerce.model.Product;

/**
 * A promotion where the second item of the same product costs half price.
 * Business Rules:
 * - Second identical product costs 50% of original price
 * - Applied for each product type separately
 */
public class SecondProductHalfPricePromotion implements Promotion {
    private static final double DISCOUNT_PERCENTAGE = 50.0;
    
    private String promotionCode;

    /**
     * Creates a new second-product-half-price promotion.
     *
     * @param promotionCode the promotion code
     */
    public SecondProductHalfPricePromotion(String promotionCode) {
        if (promotionCode == null || promotionCode.trim().isEmpty()) {
            throw new IllegalArgumentException("Promotion code cannot be empty");
        }
        
        this.promotionCode = promotionCode;
    }

    @Override
    public double calculateDiscount(Map<Product, Integer> products) {
        if (products.isEmpty()) {
            return 0;
        }
        
        double totalDiscount = 0;
        
        // For each product type, calculate how many pairs we have
        for (Map.Entry<Product, Integer> entry : products.entrySet()) {
            Product product = entry.getKey();
            int quantity = entry.getValue();
            
            // Calculate number of complete pairs (2 identical products)
            int pairs = quantity / 2;
            
            // For each pair, the discount is half the product price
            totalDiscount += pairs * (product.getPrice() * DISCOUNT_PERCENTAGE / 100.0);
        }
        
        return totalDiscount;
    }

    @Override
    public String getPromotionCode() {
        return promotionCode;
    }
} 