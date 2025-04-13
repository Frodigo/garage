package com.simple.ecommerce.infrastructure.promotion;

import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Product;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

/**
 * A promotion that applies a special price to every nth product in the cart.
 * Business Rules:
 * - Every third product costs 1 PLN
 * - Applied to cheapest products first
 */
public class CheapestProductPromotion implements PromotionStrategy {
    private static final int DEFAULT_PRODUCTS_REQUIRED = 3;
    private static final double DEFAULT_SPECIAL_PRICE = 1.0;

    private final String promotionCode;
    private final double specialPrice;
    private final int productsRequired;

    /**
     * Creates a promotion where every third product costs 1 PLN.
     *
     * @param promotionCode the promotion code
     */
    public CheapestProductPromotion(String promotionCode) {
        this(promotionCode, DEFAULT_SPECIAL_PRICE, DEFAULT_PRODUCTS_REQUIRED);
    }

    /**
     * Creates a promotion with custom parameters.
     *
     * @param promotionCode the promotion code
     * @param specialPrice the special price for the cheapest product
     * @param productsRequired the number of products required to activate the promotion
     */
    public CheapestProductPromotion(String promotionCode, double specialPrice, int productsRequired) {
        if (promotionCode == null || promotionCode.trim().isEmpty()) {
            throw new IllegalArgumentException("Promotion code cannot be empty");
        }
        if (specialPrice < 0) {
            throw new IllegalArgumentException("Special price cannot be negative");
        }
        if (productsRequired < 2) {
            throw new IllegalArgumentException("Products required must be at least 2");
        }

        this.promotionCode = promotionCode;
        this.specialPrice = specialPrice;
        this.productsRequired = productsRequired;
    }

    @Override
    public double calculateDiscount(Map<Product, Integer> products) {
        if (products.isEmpty()) {
            return 0;
        }

        // Expand the cart into a list of individual products
        List<Product> allProducts = new ArrayList<>();
        products.forEach((product, quantity) -> {
            for (int i = 0; i < quantity; i++) {
                allProducts.add(product);
            }
        });

        // If we don't have enough products, no discount applies
        if (allProducts.size() < productsRequired) {
            return 0;
        }

        // Sort products by price (cheapest first)
        allProducts.sort(Comparator.comparing(Product::getPrice));

        double totalDiscount = 0;

        // Apply the discount to every Nth product (where N = productsRequired)
        for (int i = 0; i < allProducts.size(); i++) {
            if ((i + 1) % productsRequired == 0) { // Every Nth product gets the discount
                Product discountedProduct = allProducts.get(i);
                // Discount is the difference between original price and special price
                double productDiscount = discountedProduct.getPrice() - specialPrice;
                // Ensure discount is not negative (special price doesn't exceed product price)
                if (productDiscount > 0) {
                    totalDiscount += productDiscount;
                }
            }
        }

        return totalDiscount;
    }

    @Override
    public String getPromotionCode() {
        return promotionCode;
    }
}
