package com.simple.ecommerce.promotion;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.simple.ecommerce.model.Category;
import com.simple.ecommerce.model.Product;

public class PromotionTest {
    
    private Category electronics;
    private Product laptop;
    private Product smartphone;
    private Product headphones;
    private Map<Product, Integer> cart;
    
    @Before
    public void setup() {
        electronics = new Category("Electronics");
        laptop = new Product("Laptop", 1200.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
        headphones = new Product("Headphones", 150.0, electronics);
        
        cart = new HashMap<>();
    }
    
    @Test
    public void testPercentagePromotion() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        PercentagePromotion promotion = new PercentagePromotion("10PERCENTOFF");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        double expectedDiscount = (1200.0 + 800.0) * 0.1; // 10% of 2000
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testPercentagePromotionWithCustomPercentage() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        PercentagePromotion promotion = new PercentagePromotion("20PERCENTOFF", 20.0);
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        double expectedDiscount = (1200.0 + 800.0) * 0.2; // 20% of 2000
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testCheapestProductPromotion() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        cart.put(headphones, 1);
        CheapestProductPromotion promotion = new CheapestProductPromotion("EVERY3RD1PLN");
        
        // Create a list to simulate how the promotion works
        List<Product> products = new ArrayList<>();
        products.add(headphones); // First added (cheapest)
        products.add(smartphone); // Second added
        products.add(laptop);     // Third added - this gets the discount
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        // The 3rd product gets the discount, which is laptop
        double expectedDiscount = laptop.getPrice() - 1.0; // Laptop price - 1 PLN
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testCheapestProductPromotionWithMultipleProducts() {
        // given
        cart.put(laptop, 2);
        cart.put(smartphone, 2);
        cart.put(headphones, 2);
        CheapestProductPromotion promotion = new CheapestProductPromotion("EVERY3RD1PLN");
        
        // Create a list to simulate how the promotion sorts and applies the discount
        List<Product> products = new ArrayList<>();
        // First 3 products
        products.add(headphones); // #1 cheapest
        products.add(headphones); // #2
        products.add(smartphone); // #3 - gets discount
        // Next 3 products
        products.add(smartphone); // #4
        products.add(laptop);     // #5
        products.add(laptop);     // #6 - gets discount
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        // Products #3 and #6 get the discount (smartphone and laptop)
        double expectedDiscount = (smartphone.getPrice() - 1.0) + (laptop.getPrice() - 1.0);
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testCheapestProductPromotionWithNotEnoughProducts() {
        // given
        cart.put(laptop, 1);
        cart.put(smartphone, 1);
        CheapestProductPromotion promotion = new CheapestProductPromotion("EVERY3RD1PLN");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        assertEquals(0.0, discount, 0.001); // Not enough products for the promotion
    }
    
    @Test
    public void testSecondProductHalfPricePromotion() {
        // given
        cart.put(laptop, 2);
        SecondProductHalfPricePromotion promotion = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        double expectedDiscount = laptop.getPrice() * 0.5; // 50% off the second laptop
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testSecondProductHalfPricePromotionWithMultipleProducts() {
        // given
        cart.put(laptop, 2);
        cart.put(smartphone, 3);
        SecondProductHalfPricePromotion promotion = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        // 1 pair of laptops, 1 pair of smartphones
        double expectedDiscount = (laptop.getPrice() * 0.5) + (smartphone.getPrice() * 0.5);
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test
    public void testSecondProductHalfPricePromotionWithOddQuantities() {
        // given
        cart.put(laptop, 3);
        cart.put(smartphone, 1);
        SecondProductHalfPricePromotion promotion = new SecondProductHalfPricePromotion("SECONDHALFPRICE");
        
        // when
        double discount = promotion.calculateDiscount(cart);
        
        // then
        // 1 pair of laptops (3rd laptop doesn't get discount), 0 pairs of smartphones
        double expectedDiscount = laptop.getPrice() * 0.5;
        assertEquals(expectedDiscount, discount, 0.001);
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPromotionWithEmptyCode() {
        // when
        new PercentagePromotion("");
        
        // then
        // exception is expected
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testPercentagePromotionWithInvalidPercentage() {
        // when
        new PercentagePromotion("INVALID", -10.0);
        
        // then
        // exception is expected
    }
} 