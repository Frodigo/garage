package com.simple.ecommerce.application.service;

import com.simple.ecommerce.application.exception.EmptyCartException;
import com.simple.ecommerce.application.exception.ProductUnavailableException;
import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Product;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * Service for managing shopping cart operations.
 * Business Rules:
 * - Initially empty
 * - Can have multiple units of same product
 * - Total price = sum of product prices with applied promotion
 * - Only one active promotion at a time
 * - New promotion overrides previous one
 */
public class ShoppingCartService {
    
    private final Map<Product, Integer> products;
    private PromotionStrategy activePromotion;

    /**
     * Creates an empty shopping cart service.
     */
    public ShoppingCartService() {
        this.products = new HashMap<>();
    }

    /**
     * Adds a product to the cart. If the product is already in the cart,
     * the quantity is increased by 1.
     *
     * @param product the product to add
     * @throws IllegalArgumentException if product is null
     * @throws ProductUnavailableException if product is unavailable
     */
    public void addProduct(Product product) {
        if (product == null) {
            throw new IllegalArgumentException("Product cannot be null");
        }
        
        if (!product.isAvailable()) {
            throw new ProductUnavailableException(product);
        }
        
        products.put(product, products.getOrDefault(product, 0) + 1);
    }

    /**
     * Removes a product from the cart. If the product has multiple units,
     * only one unit is removed.
     *
     * @param product the product to remove
     * @throws IllegalArgumentException if product is null
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
     * @throws EmptyCartException if the cart is empty
     */
    public double calculateCartPrice() {
        if (products.isEmpty()) {
            throw new EmptyCartException("Cannot calculate price for an empty cart");
        }
        
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
    public void activatePromotion(PromotionStrategy promotion) {
        this.activePromotion = promotion;
    }
    
    /**
     * Checks if the cart is empty.
     *
     * @return true if cart is empty, false otherwise
     */
    public boolean isEmpty() {
        return products.isEmpty();
    }
    
    /**
     * Clears all products from the cart.
     */
    public void clear() {
        products.clear();
    }
} 