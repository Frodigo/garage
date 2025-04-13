package com.simple.ecommerce.infrastructure.promotion;

import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.simple.ecommerce.application.port.PromotionStrategy;
import com.simple.ecommerce.domain.entity.Category;
import com.simple.ecommerce.domain.entity.Product;

public class CheapestProductPromotionTest {

    private Category electronics;
    private Product laptop;
    private Product tablet;
    private Product smartphone;
    private Product cheapProduct;
    private Map<Product, Integer> cart;

    @Before
    public void setup() {
        electronics = new Category("Electronics");
        laptop = new Product("Laptop", 1200.0, electronics);
        tablet = new Product("Tablet", 500.0, electronics);
        smartphone = new Product("Smartphone", 800.0, electronics);
        cheapProduct = new Product("Cheap Cable", 5.0, electronics);

        cart = new HashMap<>();
    }

    @Test
    public void testCheapestProductPromotionWithDefaultValues() {
        // given
        cart.put(laptop, 1);
        cart.put(tablet, 1);
        cart.put(smartphone, 1);
        PromotionStrategy promotion = new CheapestProductPromotion("EVERY3RD1PLN");

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // We have 3 products (sorted by price): tablet(500), smartphone(800), laptop(1200)
        // Every 3rd product gets the discount (laptop)
        // Discount for laptop = 1200 - 1 = 1199
        double expectedDiscount = 1199.0;
        assertEquals(expectedDiscount, discount, 0.001);
    }

    @Test
    public void testCheapestProductPromotionWithLessThanRequiredProducts() {
        // given
        cart.put(laptop, 1);
        cart.put(tablet, 1);
        PromotionStrategy promotion = new CheapestProductPromotion("EVERY3RD1PLN");

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // We only have 2 products, but need 3 for the promotion to apply
        assertEquals(0.0, discount, 0.001);
    }

    @Test
    public void testCheapestProductPromotionWithMultipleDiscounts() {
        // given
        cart.put(laptop, 2);
        cart.put(tablet, 3);
        cart.put(smartphone, 1);
        PromotionStrategy promotion = new CheapestProductPromotion("EVERY3RD1PLN");

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // We have 6 products, so 2 will get discounted (every 3rd)
        // Sorted by price: tablet(500), tablet(500), tablet(500), smartphone(800), laptop(1200), laptop(1200)
        // Discounted: 3rd item = tablet(500), 6th item = laptop(1200)
        // Total discount: (500-1) + (1200-1) = 499 + 1199 = 1698
        double expectedDiscount = 1698.0;
        assertEquals(expectedDiscount, discount, 0.001);
    }

    @Test
    public void testCheapestProductPromotionWithCustomValues() {
        // given
        cart.put(laptop, 1);
        cart.put(tablet, 1);
        cart.put(smartphone, 1);
        PromotionStrategy promotion = new CheapestProductPromotion("CUSTOM", 50.0, 2);

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // Every 2nd product gets the discount
        // Sorted by price: tablet(500), smartphone(800), laptop(1200)
        // Discounted: smartphone(800)
        // Total discount: 800 - 50 = 750
        double expectedDiscount = 750.0;
        assertEquals(expectedDiscount, discount, 0.001);
    }

    @Test
    public void testNoNegativeDiscountWhenSpecialPriceExceedsProductPrice() {
        // given
        // Cheap product costs only 5.0
        cart.put(cheapProduct, 3);
        // Special price is higher than the product price
        PromotionStrategy promotion = new CheapestProductPromotion("EXPENSIVE_SPECIAL", 10.0, 3);

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // Every 3rd product gets the discount (cheapProduct)
        // But since 5 - 10 would be negative, no discount should be applied
        double expectedDiscount = 0.0;
        assertEquals(expectedDiscount, discount, 0.001);

        // Additional verification: the total discount should never be negative
        assertTrue("Discount should never be negative", discount >= 0.0);
    }

    @Test
    public void testMixedProductPricesWithSpecialPriceHigherThanSome() {
        // given
        cart.put(cheapProduct, 2); // 5.0 each, less than special price
        cart.put(tablet, 2);       // 500.0 each, more than special price
        cart.put(laptop, 2);       // 1200.0 each, more than special price

        // Special price that's higher than cheapProduct but lower than others
        PromotionStrategy promotion = new CheapestProductPromotion("MIXED_CASE", 7.0, 2);

        // when
        double discount = promotion.calculateDiscount(cart);

        // then
        // Sorted by price: cheapProduct(5.0), cheapProduct(5.0), tablet(500), tablet(500), laptop(1200), laptop(1200)
        // Every 2nd product gets the discount: cheapProduct(5.0), tablet(500), laptop(1200)
        // cheapProduct discount would be negative, so it's ignored
        // Discounts: 0 + (500-7) + (1200-7) = 0 + 493 + 1193 = 1686
        double expectedDiscount = 1686.0;
        assertEquals(expectedDiscount, discount, 0.001);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNegativeSpecialPrice() {
        // when
        new CheapestProductPromotion("INVALID", -10.0, 3);

        // then
        // exception is expected
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidProductsRequired() {
        // when
        new CheapestProductPromotion("INVALID", 10.0, 1);

        // then
        // exception is expected
    }
}
