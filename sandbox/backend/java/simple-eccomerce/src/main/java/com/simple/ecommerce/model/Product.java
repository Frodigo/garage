package com.simple.ecommerce.model;

/**
 * Represents a product in the eCommerce system.
 * Business Rules:
 * - Must have name, price and category
 * - Can be marked available or unavailable
 */
public class Product {
    private String name;
    private double price;
    private Category category;
    private boolean available;

    /**
     * Creates a new product with the specified attributes.
     *
     * @param name     the product name
     * @param price    the product price
     * @param category the product category
     */
    public Product(String name, double price, Category category) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Product name cannot be empty");
        }
        if (price < 0) {
            throw new IllegalArgumentException("Product price cannot be negative");
        }
        if (category == null) {
            throw new IllegalArgumentException("Product category cannot be null");
        }

        this.name = name;
        this.price = price;
        this.category = category;
        this.available = true; // By default, products are available
    }

    /**
     * Returns the product name.
     *
     * @return the product name
     */
    public String getName() {
        return name;
    }

    /**
     * Returns the product price.
     *
     * @return the product price
     */
    public double getPrice() {
        return price;
    }

    /**
     * Returns the product category.
     *
     * @return the product category
     */
    public Category getCategory() {
        return category;
    }

    /**
     * Checks if the product is available.
     *
     * @return true if the product is available, false otherwise
     */
    public boolean isAvailable() {
        return available;
    }

    /**
     * Sets the product availability status.
     *
     * @param available the availability status to set
     */
    public void setAvailable(boolean available) {
        this.available = available;
    }

    @Override
    public String toString() {
        return name + " ($" + price + ")";
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Product product = (Product) obj;
        return name.equals(product.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }
} 