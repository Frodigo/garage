package com.simple.ecommerce.model;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.simple.ecommerce.promotion.Promotion;

/**
 * Represents a shopping cart in the eCommerce system.
 * Business Rules:
 * - Initially empty
 * - Can have multiple units of same product
 * - Total price = sum of product prices with applied promotion
 * - Only one active promotion at a time
 * - New promotion overrides previous one
 */
public class ShoppingCart {
    private Map<Product, Integer> products;
    private Promotion activePromotion;

    /**
     * Creates an empty shopping cart.
     */
    public ShoppingCart() {
        this.products = new HashMap<>();
    }

    /**
     * Adds a product to the cart. If the product is already in the cart,
     * the quantity is increased by 1.
     *
     * @param product the product to add
     */
    public void addProduct(Product product) {
        if (product == null) {
            throw new IllegalArgumentException("Product cannot be null");
        }
        
        if (!product.isAvailable()) {
            throw new IllegalArgumentException("Cannot add unavailable product to cart: " + product.getName());
        }
        
        products.put(product, products.getOrDefault(product, 0) + 1);
    }

    /**
     * Removes a product from the cart. If the product has multiple units,
     * only one unit is removed.
     *
     * @param product the product to remove
     */
    public void removeProduct(Product product) {
        if (product == null) {
            throw new IllegalArgumentException("Product cannot be null");
        }
        
        if (!products.containsKey(product)) {
            return; // Product not in cart, nothing to remove
        }
        
        int quantity = products.get(product);
        if (quantity > 1) {
            products.put(product, quantity - 1);
        } else {
            products.remove(product);
        }
    }

    /**
     * Returns the contents of the cart.
     *
     * @return an unmodifiable map of products and their quantities
     */
    public Map<Product, Integer> getCartContents() {
        return Collections.unmodifiableMap(products);
    }

    /**
     * Calculates the total price of all products in the cart,
     * applying any active promotion.
     *
     * @return the total price
     */
    public double calculateCartPrice() {
        double totalPrice = products.entrySet().stream()
                .mapToDouble(entry -> entry.getKey().getPrice() * entry.getValue())
                .sum();
        
        if (activePromotion != null) {
            double discount = activePromotion.calculateDiscount(products);
            return Math.max(0, totalPrice - discount);
        }
        
        return totalPrice;
    }

    /**
     * Activates a promotion for this cart. Any previously active promotion is overridden.
     *
     * @param promotion the promotion to activate
     */
    public void activatePromotion(Promotion promotion) {
        this.activePromotion = promotion;
    }
} 