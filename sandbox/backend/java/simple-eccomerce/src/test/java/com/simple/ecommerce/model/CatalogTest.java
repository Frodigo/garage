package com.simple.ecommerce.model;

import static org.junit.Assert.*;

import java.util.List;

import org.junit.Before;
import org.junit.Test;

public class CatalogTest {
    
    private Catalog catalog;
    private Category electronics;
    private Category books;
    private Product laptop;
    private Product tablet;
    private Product smartphone;
    private Product book;
    
    @Before
    public void setup() {
        catalog = new Catalog();
        electronics = new Category("Electronics");
        books = new Category("Books");
        
        laptop = new Product("Laptop", 1200.0, electronics);
        tablet = new Product("Tablet", 500.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
        book = new Product("Java Programming", 45.0, books);
        
        catalog.addProduct(laptop);
        catalog.addProduct(tablet);
        catalog.addProduct(smartphone);
        catalog.addProduct(book);
    }
    
    @Test
    public void testGetAllProducts() {
        // when
        List<Product> allProducts = catalog.getAllProducts();
        
        // then
        assertEquals(4, allProducts.size());
        assertTrue(allProducts.contains(laptop));
        assertTrue(allProducts.contains(tablet));
        assertTrue(allProducts.contains(smartphone));
        assertTrue(allProducts.contains(book));
    }
    
    @Test
    public void testGetProductsSortedAlphabetically() {
        // when
        List<Product> sortedProducts = catalog.getProductsSortedAlphabetically();
        
        // then
        assertEquals(4, sortedProducts.size());
        assertEquals("Java Programming", sortedProducts.get(0).getName());
        assertEquals("Laptop", sortedProducts.get(1).getName());
        assertEquals("Smartphone", sortedProducts.get(2).getName());
        assertEquals("Tablet", sortedProducts.get(3).getName());
    }
    
    @Test
    public void testGetAvailableProductsByCategory() {
        // when
        List<Product> electronicsProducts = catalog.getAvailableProductsByCategory(electronics);
        
        // then
        assertEquals(3, electronicsProducts.size());
        assertEquals("Tablet", electronicsProducts.get(0).getName()); // Cheapest first
        assertEquals("Smartphone", electronicsProducts.get(1).getName());
        assertEquals("Laptop", electronicsProducts.get(2).getName()); // Most expensive last
    }
    
    @Test
    public void testGetAvailableProductsByCategoryWithUnavailableProducts() {
        // given
        smartphone.setAvailable(false);
        
        // when
        List<Product> electronicsProducts = catalog.getAvailableProductsByCategory(electronics);
        
        // then
        assertEquals(2, electronicsProducts.size());
        assertTrue(electronicsProducts.contains(laptop));
        assertTrue(electronicsProducts.contains(tablet));
        assertFalse(electronicsProducts.contains(smartphone)); // Unavailable, should not be included
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testAddNullProduct() {
        // when
        catalog.addProduct(null);
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testGetAvailableProductsByNullCategory() {
        // when
        catalog.getAvailableProductsByCategory(null);
        
        // then
        // exception is expected
    }
} 