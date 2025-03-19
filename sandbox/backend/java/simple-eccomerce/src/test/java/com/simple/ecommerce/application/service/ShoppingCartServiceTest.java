package com.simple.ecommerce.application.service;

import static org.junit.Assert.*;

import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;
import com.simple.ecommerce.infrastructure.promotion.PercentagePromotion;
import com.simple.ecommerce.infrastructure.promotion.SecondProductHalfPricePromotion;

public class ShoppingCartServiceTest {
    
    private ShoppingCartService cart;
    private Category electronics;
    private Product laptop;
    private Product tablet;
    private Product smartphone;
    
    @Before
    public void setup() {
        cart = new ShoppingCartService();
        electronics = new Category("Electronics");
        
        laptop = new Product("Laptop", 1200.0, electronics);
        tablet = new Product("Tablet", 500.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
    }
    
    @Test
    public void testAddProduct() {
        // when
        cart.addProduct(laptop);
        
        // then
        Map<Product, Integer> contents = cart.getCartContents();
        assertEquals(1, contents.size());
        assertEquals(Integer.valueOf(1), contents.get(laptop));
        
        // when adding the same product again
        cart.addProduct(laptop);
        
        // then
        contents = cart.getCartContents();
        assertEquals(1, contents.size());
        assertEquals(Integer.valueOf(2), contents.get(laptop));
    }
    
    @Test
    public void testAddMultipleProducts() {
        // when
        cart.addProduct(laptop);
        cart.addProduct(tablet);
        cart.addProduct(smartphone);
        
        // then
        Map<Product, Integer> contents = cart.getCartContents();
        assertEquals(3, contents.size());
        assertEquals(Integer.valueOf(1), contents.get(laptop));
        assertEquals(Integer.valueOf(1), contents.get(tablet));
        assertEquals(Integer.valueOf(1), contents.get(smartphone));
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testAddNullProduct() {
        // when
        cart.addProduct(null);
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testAddUnavailableProduct() {
        // given
        laptop.setAvailable(false);
        
        // when
        cart.addProduct(laptop);
        
        // then
        // exception is expected
    }
    
    @Test
    public void testRemoveProduct() {
        // given
        cart.addProduct(laptop);
        cart.addProduct(laptop);
        cart.addProduct(tablet);
        
        // when
        cart.removeProduct(laptop);
        
        // then
        Map<Product, Integer> contents = cart.getCartContents();
        assertEquals(2, contents.size());
        assertEquals(Integer.valueOf(1), contents.get(laptop));
        assertEquals(Integer.valueOf(1), contents.get(tablet));
        
        // when removing again
        cart.removeProduct(laptop);
        
        // then
        contents = cart.getCartContents();
        assertEquals(1, contents.size());
        assertFalse(contents.containsKey(laptop));
        assertEquals(Integer.valueOf(1), contents.get(tablet));
    }
    
    @Test
    public void testRemoveNonExistentProduct() {
        // given
        cart.addProduct(laptop);
        
        // when
        cart.removeProduct(tablet); // Not in cart
        
        // then
        Map<Product, Integer> contents = cart.getCartContents();
        assertEquals(1, contents.size());
        assertEquals(Integer.valueOf(1), contents.get(laptop));
    }
    
    @Test
    public void testCalculateCartPrice() {
        // given
        cart.addProduct(laptop);
        cart.addProduct(tablet);
        
        // when
        double totalPrice = cart.calculateCartPrice();
        
        // then
        assertEquals(1700.0, totalPrice, 0.001); // 1200 + 500
    }
    
    @Test
    public void testCalculateCartPriceWithPercentagePromotion() {
        // given
        cart.addProduct(laptop);
        cart.addProduct(tablet);
        PromotionStrategy tenPercentOff = new PercentagePromotion("10PERCENTOFF");
        
        // when
        cart.activatePromotion(tenPercentOff);
        double discountedPrice = cart.calculateCartPrice();
        
        // then
        double expectedPrice = 1700.0 * 0.9; // 10% off 1700
        assertEquals(expectedPrice, discountedPrice, 0.001);
    }
    
    @Test
    public void testCalculateCartPriceWithSecondProductHalfPricePromotion() {
        // given
        cart.addProduct(laptop);
        cart.addProduct(laptop); // Second laptop
        PromotionStrategy secondHalfPrice = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        
        // when
        cart.activatePromotion(secondHalfPrice);
        double discountedPrice = cart.calculateCartPrice();
        
        // then
        double expectedPrice = 1200.0 + (1200.0 * 0.5); // First laptop + half price second laptop
        assertEquals(expectedPrice, discountedPrice, 0.001);
    }
    
    @Test
    public void testActivatePromotion() {
        // given
        cart.addProduct(laptop);
        cart.addProduct(tablet);
        PromotionStrategy tenPercentOff = new PercentagePromotion("10PERCENTOFF");
        
        // when
        cart.activatePromotion(tenPercentOff);
        double discountedPrice1 = cart.calculateCartPrice();
        
        // New promotion overrides the previous one
        PromotionStrategy secondHalfPrice = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        cart.activatePromotion(secondHalfPrice);
        double discountedPrice2 = cart.calculateCartPrice();
        
        // then
        double expectedPrice1 = 1700.0 * 0.9; // 10% off 1700
        assertEquals(expectedPrice1, discountedPrice1, 0.001);
        
        // With the second promotion, no discount applies since there are no pairs of the same product
        assertEquals(1700.0, discountedPrice2, 0.001);
    }
} 