package com.simple.ecommerce.application.service;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.List;

import org.junit.Before;
import org.junit.Test;

import com.simple.ecommerce.application.exception.CategoryNotFoundException;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.domain.repository.ProductRepository;
import com.simple.ecommerce.infrastructure.persistence.InMemoryProductRepository;

public class CatalogServiceTest {

    private CatalogService catalogService;
    private ProductRepository productRepository;
    private Category electronics;
    private Category books;
    private Product laptop;
    private Product tablet;
    private Product smartphone;
    private Product book;

    @Before
    public void setup() {
        productRepository = new InMemoryProductRepository();
        catalogService = new CatalogService(productRepository);

        electronics = new Category("Electronics");
        books = new Category("Books");

        laptop = new Product("Laptop", 1200.0, electronics);
        tablet = new Product("Tablet", 500.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
        book = new Product("Java Programming", 45.0, books);

        catalogService.addProduct(laptop);
        catalogService.addProduct(tablet);
        catalogService.addProduct(smartphone);
        catalogService.addProduct(book);
    }

    @Test
    public void testGetAllProducts() {
        // when
        List<Product> allProducts = catalogService.getAllProducts();

        // then
        assertEquals(4, allProducts.size());
        assertTrue(allProducts.containsAll(Arrays.asList(laptop, tablet, smartphone, book)));
    }

    @Test
    public void testGetProductsSortedAlphabetically() {
        // when
        List<Product> sortedProducts = catalogService.getProductsSortedAlphabetically();

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
        List<Product> electronicsProducts = catalogService.getAvailableProductsByCategory(electronics);

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
        List<Product> electronicsProducts = catalogService.getAvailableProductsByCategory(electronics);

        // then
        assertEquals(2, electronicsProducts.size());
        assertTrue(electronicsProducts.contains(laptop));
        assertTrue(electronicsProducts.contains(tablet));
        assertFalse(electronicsProducts.contains(smartphone)); // Unavailable, should not be included
    }

    @Test(expected = IllegalArgumentException.class)
    public void testConstructorWithNullRepository() {
        // when
        new CatalogService(null);

        // then
        // exception is expected
    }

    @Test(expected = CategoryNotFoundException.class)
    public void testGetAvailableProductsByNullCategory() {
        // when
        catalogService.getAvailableProductsByCategory(null);

        // then
        // exception is expected
    }
}
