package com.simple.ecommerce.domain.entity;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

public class ProductTest {

    private Category category;

    @Before
    public void setup() {
        category = new Category("Electronics");
    }

    @Test
    public void testProductCreation() {
        // given
        String name = "Laptop";
        double price = 1200.0;

        // when
        Product product = new Product(name, price, category);

        // then
        assertEquals(name, product.getName());
        assertEquals(price, product.getPrice(), 0.001);
        assertEquals(category, product.getCategory());
        assertTrue(product.isAvailable());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testProductCreationWithNullName() {
        // given
        String name = null;
        double price = 1200.0;

        // when
        new Product(name, price, category);

        // then
        // exception is expected
    }

    @Test(expected = IllegalArgumentException.class)
    public void testProductCreationWithEmptyName() {
        // given
        String name = "";
        double price = 1200.0;

        // when
        new Product(name, price, category);

        // then
        // exception is expected
    }

    @Test(expected = IllegalArgumentException.class)
    public void testProductCreationWithNegativePrice() {
        // given
        String name = "Laptop";
        double price = -100.0;

        // when
        new Product(name, price, category);

        // then
        // exception is expected
    }

    @Test(expected = IllegalArgumentException.class)
    public void testProductCreationWithNullCategory() {
        // given
        String name = "Laptop";
        double price = 1200.0;

        // when
        new Product(name, price, null);

        // then
        // exception is expected
    }

    @Test
    public void testSetAvailable() {
        // given
        Product product = new Product("Laptop", 1200.0, category);
        assertTrue(product.isAvailable());

        // when
        product.setAvailable(false);

        // then
        assertFalse(product.isAvailable());

        // when
        product.setAvailable(true);

        // then
        assertTrue(product.isAvailable());
    }

    @Test
    public void testEquals() {
        // given
        Product laptop1 = new Product("Laptop", 1200.0, category);
        Product laptop2 = new Product("Laptop", 1300.0, category);
        Product tablet = new Product("Tablet", 500.0, category);

        // then
        assertEquals(laptop1, laptop2); // Same name, different price
        assertNotEquals(laptop1, tablet);
    }
}
