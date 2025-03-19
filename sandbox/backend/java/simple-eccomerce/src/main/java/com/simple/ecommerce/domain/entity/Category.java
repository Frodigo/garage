package com.simple.ecommerce.domain.entity;

/**
 * Represents a product category in the store.
 */
public class Category {
    private String name;

    /**
     * Creates a new category with the specified name.
     * 
     * @param name the category name
     */
    public Category(String name) {
        this.name = name;
    }

    /**
     * Returns the category name.
     * 
     * @return the category name
     */
    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Category category = (Category) obj;
        return name.equals(category.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }
} 