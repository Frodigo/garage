*Published at 29/12/2021*

## Magento 2 product types

There are six types of products in Magento:

- simple products

- grouped products

- bundle products

- configurable products

- virtual products

- downloadable Products

---

### Simple products

Simple Product is the most frequently used product type by store owners. Every such Product is considered a single item that is not subject to customization.

For instance, a book. Every Simple Product is a physical item and has an SKU (Store Keeping Unit) number.

Every single product has a set of attributes that you can set up in the admin panel. A simple product is a standalone product that can be sold separately or as a part of grouped Product, Configurable Product, or bundle product.

---

### Grouped products

Magento Grouped Product is a collection of Simple Products that can be bought together. For instance, someone buying a table may also be interested in complementary chairs.

You can create Grouped Products including a table and chairs and offer a discount. Your customer will be able to pay less when buying the set.

Products that are part of the grouped Product can be purchased together or separately. Take a look at the example grouped Product: Set of Sprite Yoga Straps:

As you can see, the Set of Sprite Yoga Straps grouped Product is a set of three simple products:

- Sprite Yoga Strap 6 foot

- Sprite Yoga Strap 8 foot

- Sprite Yoga Strap 10 foot

---

### Bundle products

Bundle Product is a collection of similar products that differ in some detail. For instance, if a customer is looking for headphones, you can offer him five types of those that come from different manufacturers and are listed at different prices.

Your customer will surely appreciate that he's being presented with various options to choose from.

Another example is bundle product from default Magento 2 demo: Sprite yoga companion kit. When a customer goes to the product catalog and then to the Sprite yoga companion kit's product page, there is a "Customize and add to cart" button.

Then a customer can choose the type of ball and strap. Change the quantity of all simple products included in bundled product.

Grouped and bundle products in Magento 2 are beneficial types of products, and thanks to them, you can increase the sale of your products.

---

### Configurable products

Magento Configurable Product is a product type that allows you to post products that offer additional options to consider before purchasing.

Configurable Products in Magento are collections of Simple Products. A Configurable Product isn't an actual item in your store and doesn't come on its own.

A Configurable Product is a kind of container for Simple Products, allowing the customer to modify them to their liking.

To generate product variations for a configurable product, Magento 2 creates simple products. Each variation is a simple product that is not visible in the product catalog individually.

An excellent example of a Configurable Product is a shirt, where you can select its size and color.

Thanks to Magento's Configurable Products mechanism, the customer can customize some of the Product's elements.

---

### Downloadable Products

A downloadable product is a product that the customer can (surprise) download right after purchasing.

An e-book may serve as an example in this category. The customer expects that after he pays, he'll be able to download the Product to his hard drive.

An example of an excellent downloadable product is a Beginner's Yoga video from Magento 2 demo.

When customers buy a downloadable product, downloadable files will be visible on the "My downloadable products" page in a Customer account.

---

### Virtual products

Magento Virtual Product is the one that can't be downloaded or shipped. Virtual Product is mostly additional service related to the particular Product.

For instance, when buying a PC, you can purchase an extra warranty extension - this is what a Virtual Product is.

On the other hand, a virtual product is simple without weight. When customers buy a virtual product and go to checkout - there is no shipping step.

Simple and virtual products are pretty similar, but it's clear that digital Product does not have weight.

---

## Other product types in Magento 2

### Up sells, related, and cross-sell products

Those listed above are products that are associated with other standalone products.

On the product page, you can see related and up-sell products. Related products are products similar to the main Product, and up-sell is identical as well, but they have higher prices.

Cross-sell products appear in the cart. For example, if you buy shoes, socks can be a cross-sell product.

### Custom options

Product in Magento can have customizable options that allow offering a selection of options with a variety of text, selection, and date input types.

For example, you can sell licenses for your online course, and there can be three types of licenses. Basic, Standard, and Pro. Each one can have a different price.

## Support for product types in Magento headless solutions

There are two main headless storefronts available for Magento 2: PWA Studio and Vue Storefront.

Let's look at how support for different Magento products looks in those headless storefronts.

| Product type | Magento Monolith | PWA Studio | Vue Storefront - Magento 2 integration \[beta\] |
| ------------ | ---------------- | ---------- | ----------------------------------------------- |
| Simple       | yes              | yes        | yes                                             |
| Grouped      | yes              | no         | yes                                             |
| Configurable | yes              | yes        | yes                                             |
| Bundle       | yes              | no         | yes                                             |
| Downloadable | yes              | no         | partial                                         |
| Virtual      | yes              | no         | partial                                         |

Magento Luma is a benchmark for headless, and I hope that headless approaches will shortly support all Magento product types. Anyway, if you don't need support for virtual and downloadable products, VSF can be an option for you even now.

---

## Conclusion

Magento 2 provides pretty extensive options when it comes to creating products. This will help you switch things up and diversify the product range offered at your Magento 2 online store to meet the customers' expectations.
Headless solutions are behind Magento Monolith in terms of support for product types, but it's only a matter of time when full support will be in place.
