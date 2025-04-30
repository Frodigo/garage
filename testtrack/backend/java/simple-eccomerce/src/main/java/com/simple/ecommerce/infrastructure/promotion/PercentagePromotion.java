package com.simple.ecommerce.infrastructure.promotion;

import com.simple.ecommerce.application.exception.EmptyCartException;
import com.simple.ecommerce.application.exception.InvalidPromotionException;
import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Product;

import java.util.Map;

/**
 * Applies a percentage discount to the entire cart.
 * Business Rules:
 * - Applies 10% discount to entire cart
 */
public class PercentagePromotion implements PromotionStrategy {
    private static final double DEFAULT_DISCOUNT_PERCENTAGE = 10.0;

    private final String promotionCode;
    private final double discountPercentage;

    /**
     * Creates a new percentage promotion with the default 10% discount.
     *
     * @param promotionCode the promotion code
     * @throws InvalidPromotionException if the promotion code is invalid
     */
    public PercentagePromotion(String promotionCode) {
        this(promotionCode, DEFAULT_DISCOUNT_PERCENTAGE);
    }

    /**
     * Creates a new percentage promotion with a custom discount percentage.
     *
     * @param promotionCode the promotion code
     * @param discountPercentage the discount percentage (0-100)
     * @throws InvalidPromotionException if the promotion code is invalid or discount is out of range
     */
    public PercentagePromotion(String promotionCode, double discountPercentage) {
        if (promotionCode == null || promotionCode.trim().isEmpty()) {
            throw new InvalidPromotionException("Promotion code cannot be empty");
        }
        if (discountPercentage < 0 || discountPercentage > 100) {
            throw new InvalidPromotionException(promotionCode,
                "Discount percentage must be between 0 and 100, got: " + discountPercentage);
        }

        this.promotionCode = promotionCode;
        this.discountPercentage = discountPercentage;
    }

    @Override
    public double calculateDiscount(Map<Product, Integer> products) {
        if (products == null || products.isEmpty()) {
            throw new EmptyCartException("Cannot calculate discount on an empty cart");
        }

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
