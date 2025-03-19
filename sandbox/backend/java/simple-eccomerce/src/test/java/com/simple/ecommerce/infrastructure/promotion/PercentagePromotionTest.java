package com.simple.ecommerce.infrastructure.promotion;

import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;

public class PercentagePromotionTest {
    
    private Category electronics;
    private Product laptop;
    private Product smartphone;
    private Map<Product, Integer> cart;
    
    @Before
    public void setup() {
        electronics = new Category("Electronics");
        laptop = new Product("Laptop", 1200.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
        
        cart = new HashMap<>();
    }
    
    @Test
    public void testPercentagePromotionWithDefaultDiscount() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        PromotionStrategy promotion = new PercentagePromotion("10PERCENTOFF");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        double expectedDiscount = (1200.0 + 800.0) * 0.1; // 10% of 2000
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testPercentagePromotionWithCustomDiscount() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        PromotionStrategy promotion = new PercentagePromotion("20PERCENTOFF", 20.0);
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        double expectedDiscount = (1200.0 + 800.0) * 0.2; // 20% of 2000
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testPercentagePromotionWithEmptyCart() {
        // given
        PromotionStrategy promotion = new PercentagePromotion("10PERCENTOFF");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        assertEquals(0.0, discount, 0.001);
    }
    
    @Test
    public void testGetPromotionCode() {
        // given
        String promotionCode = "SUMMER_SALE";
        PromotionStrategy promotion = new PercentagePromotion(promotionCode);
        
        // when
        String returnedCode = promotion.getPromotionCode();
        
        // then
        assertEquals(promotionCode, returnedCode);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPercentagePromotionWithNullCode() {
        // when
        new PercentagePromotion(null);
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPercentagePromotionWithEmptyCode() {
        // when
        new PercentagePromotion("");
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPercentagePromotionWithNegativeDiscount() {
        // when
        new PercentagePromotion("INVALID", -10.0);
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPercentagePromotionWithTooHighDiscount() {
        // when
        new PercentagePromotion("INVALID", 110.0);
        
        // then
        // exception is expected
    }
} 