---
date: 2025-02-2022
title: Magento GraphQL - How to resolve URL
---
*Last updated at 12/02/2022*

Recently  I described the basics of Magento GraphQL. This time I want to show you a practical example of how to scaffold a headless app connected with Magento GraphQL and fetch appropriate data from Magento based on a given URL. This article is about:

- concept/idea of how to create routing in a custom Magento headless project

- which GraphQL is appropriate to resolve URLs

- how to fetch information about categories, products, and CMS pages from API based on a given URL

- how to implement the URL resolving functionality in the frontend app (in the big picture)

---

## Magento GraphQL routing concept

Let me explain the idea of routing in a headless app from not the best pattern I have already seen. Typically in an eCommerce app, you have the following pages: home/cms pages, category page, product page, my account, checkout, etc.

So you can create some custom routes in a headless app to handle all of them, for example:

- Home - **baseUrl/** - to handle homepage

- Page - **baseUrl/:pageId** - to handle CMS pages

- Category - **baseUrl/category/:categoryId**

- Product - **baseUrl/product/:productId**

- Checkout - **baseUrl/checkout**

- My account - **baseUrl/account**

That solution works, but the huge disadvantage is that the URLs are not (user and SEO) friendly. In Magento Luma (Monolith version), you can visit pages like in following links:

- [https://magento2demo.frodigo.com/women.html](https://magento2demo.frodigo.com/women.html) - category page

- [https://magento2demo.frodigo.com/joust-duffle-bag.html](https://magento2demo.frodigo.com/joust-duffle-bag.html) - product page

- [https://magento2demo.frodigo.com/about-us](https://magento2demo.frodigo.com/about-us) - CMS page

---

## The route query

Fortunately, Magento GraphQL supports URL resolving for the category, product, and CMS pages. There is the route query that receives the URL key and returns information about the entity that matches the given URL key or null if it's not possible to resolve the URL.

```javascript
query resolveRoute($url: String!) {
  route(url: $url) {
    redirect_code,
    relative_url,
    type
    ... on SimpleProduct {
      sku
      url_key
      uid
      type
      name
    }
    ... on CategoryTree {
      name
      product_count
      uid
    }
    ... on CmsPage {
      identifier
      content_heading
      content
    }
  }
}
```

Complete documentation about the route query: [https://devdocs.magento.com/guides/v2.4/graphql/queries/route.html](https://devdocs.magento.com/guides/v2.4/graphql/queries/route.html)

The route query returns three fields:

- **redirect_code (Int)** \- Contains 0 when there is no redirect error. A value of 301 indicates the URL of the requested resource has been changed permanently, while a value of 302 indicates a temporary redirect.

- **relative_url (String)** \- The relative internal URL. If the specified URL is a redirect, the query returns the redirected URL, not the original

- **type (UrlRewriteEntityTypeEnum)** - One of **PRODUCT**, **CATEGORY**, or **CMS_PAGE**

The route query has one obligatory parameter: "URL," which is a string.

Moreover, the route query is implemented by SimpleProduct, DownloadableProduct, BundleProduct, GroupedProduct, VirtualProduct, ConfigurableProduct, CategoryTree, and CmsPaage so that you can get information about those entities in the route query. In the example above, I used SimpleProduct, CmsPage, and CategoryTree.

### Types of pages in Magento

Three types of URLs can be resolved using Magento GraphQL API and the route query.

#### CMS

CMS pages contain content like about us, homepage, privacy policy, etc.

Take a look at an example response for the About us page:

```json
// variables:
{
   "url": "about-us"
}

// results:
{
  "data": {
    "route": {
      "redirect_code": 0,
      "relative_url": "about-us",
      "type": "CMS_PAGE",
      "identifier": "about-us",
      "content_heading": "About us",
      "content": "<div class=\"about-info cms-content\">\n      <p class=\"cms-content-important\">With more than 230 stores spanning 43 states and growing, Luma is a nationally recognized active wear manufacturer and retailer. We’re passionate about active lifestyles – and it goes way beyond apparel.</p>\n\n      <p>At Luma, wellness is a way of life. We don’t believe age, gender or past actions define you, only your ambition and desire for wholeness... today.</p>\n\n      <p>We differentiate ourselves through a combination of unique designs and styles merged with unequaled standards of quality and authenticity. Our founders have deep roots in yoga and health communities and our selections serve amateur practitioners and professional athletes alike.</p>\n\n      <ul style=\"list-style: none; margin-top: 20px; padding: 0;\">\n          <li><a href=\"https://magento2demo.frodigo.com/contact/\">Contact Luma</a></li>\n          <li><a href=\"https://magento2demo.frodigo.com/customer-service/\">Customer Service</a></li>\n          <li><a href=\"https://magento2demo.frodigo.com/privacy-policy/\">Luma Privacy Policy</a></li>\n          <li><a href=\"https://magento2demo.frodigo.com/\">Shop Luma</a></li>\n      </ul>\n  </div>\n"
    }
  }
}
```

The following query that received the "about-us" URL returns type equals CMS_PAGE and information about the CMS page that we wanted to fetch

#### Product

Product pages present information about products. Take a look at the example "Joust Duffle Bag" product that has the "joust-duffle-bag.html" URL key:

```json
// variables:
{
   "url": "joust-duffle-bag.html"
}

// results:
{
  "data": {
    "route": {
      "redirect_code": 0,
      "relative_url": "joust-duffle-bag.html",
      "type": "PRODUCT",
      "sku": "24-MB01",
      "url_key": "joust-duffle-bag",
      "uid": "MQ==",
      "name": "Joust Duffle Bag"
    }
  }
}
```

The following query that received the "joust-duffle-bag.html" URL returns type equals PRODUCT and information about the product we wanted to fetch.

#### Category

Category pages display information about the category. Moreover, Magento has a pretty nice feature called **Category Landing Pages** that allows rendering CMS blocks (you can display any CMS content on the category page).

Take a look at examples for the women category.

```json
// variables:
{
  "url": "women.html"
}

// results:
{
  "data": {
    "route": {
      "redirect_code": 0,
      "relative_url": "women.html",
      "type": "CATEGORY",
      "name": "Women",
      "product_count": 0,
      "uid": "MjA="
    }
  }
}
```

When passing the 'women.html' URL, Magento returns the type equals CATEGORY and information about the category that we wanted to fetch

#### No route

When you pass an URL that doesn't exist in Magento, the route query will return null. Take a look at the example:

```javascript
// query:
query resolveRoute($url: String!) {
  route(url: $url) {
    redirect_code,
    relative_url,
    type
  }
}

// variables:
{
  "url": "this-is-not-exist-i-am-sure"
}

// results:
{
  "data": {
    "route": null
  }
}
```

Once you know that the URL doesn't have corresponding information in the Magento backend, you can render the 404 page.

#### Other routes

Of course, there are more types of pages in eCommerce stores, like checkout pages or customer account pages, but the three types I mentioned before are crucial in terms of SEO and how they are rendered, and what URL is used.

### Deprecated URL resolver query

Note there is the urlResolver [GraphQL query](https://marcin-kwiatkowski.com/blog/graphql/the-full-stack-guide-to-the-graphql-query) that basically does the same as the route query, but it's deprecated and should not be used.

---

## Sample implementation in a headless app

Today I want to show some pseudo-code and an idea in the big picture of how to implement URL resolving logic in a NextJS app.

Basically, for those three types of pages that can be resolved (category, product, and CMS), you can create a dynamic route in the pages directory: \[\[...slug\]\]. You can create separate routes for other pages like checkout, cart, and my-account. So your pages directory can look like this:

- pages/ \[\[...slug\]\].tsx

- pages/checkout.tsx

- pages/cart.tsx

- pages/account.tsx

That's it. All dynamic routes like category, product, and CMS will be handled by \[\[...slug\]\] route, and other pages will be operated by custom routes like the cart.tsx or account.tsx

Take a look at the pseudo-code implementation for the \[\[...slug\]\] route:

```javascript
import React, { Suspense } from 'react'
/** Route GraphQL Magento type: **/
import type { Route } from '../types/magento'

/**
 * helper to fetch data on server side
 * signature: function useData<Type>(key, fetcher): ApiData<Type>
 * returns:
 * interface ApiData<Type> {
 *   data: Type,
 *   error: Error
 * }
 */
import useData from '../lib/use-data';
/**
 * Wrapper for GraphQL function that allows to query GraphQL API
 * async <TYPE, VARIABLES>(query, variables = null): Promise<TYPE>
 */
import { query as apiQuery } from '../providers/Api';
/**
 * Route GraphQL queury:
 */
import routeQuery from "../queries/route.gql";
import Loader from "../components/Loader"; // Loaded component
import CmsPage from "../modules/cms/components/CmsPage/CmsPage.server"; // CMS Page component
import ProductPage from "../modules/product/components/ProductPage/ProductPage.server"; // Product Page component
import CategoryPage from "../modules/category/components/CategoryPage/CategoryPage.server"; // Category Page component

type RouteQuery = {
    route: Route
}

/**
 * Enum that represent three possible types of pages
 */
enum PageTypes {
    Product = 'PRODUCT',
    Category = 'CATEGORY',
    CmsPage = 'CMS_PAGE'
}

/**
 * render page content based on given type and url key
 */
const renderPageContent = (route: Route) => {
    const pages = {
        [PageTypes.CmsPage]: <CmsPage data={route}/>,
        [PageTypes.Product]: <ProductPage data={route}/>,
        [PageTypes.Category]: <CategoryPage data={route}/>,

    }

    return pages[route.type]
}

export default function slug({ router }) {
    const { query } = router;
    const slug = query?.slug ? query?.slug?.join('/') : 'home'; // handle dynamic slugs

    /**
     * Fetch route information based on slug
     */
    const { data: { route }} = useData(
        `route/${slug}`,
        () => apiQuery<RouteQuery, { url: string }>(routeQuery, { url: slug }))

    /**
     * content to render:
     */
    const content = renderPageContent(route);

    if (content === null) {
        // redirect to 404 page
    }

    return <Suspense fallback={<Loader/>}>
        {content}
    </Suspense>
}
```

I hope that the comments in the code are helpful. Besides explaining that code, I would say I use **React Server Components** (experimental). RSC allows the rendering of React components on the server-side. Because of that, components there has a \`.server\` prefix. Server components are game-changers in frontend development, and I can't wait where they will be released as stable features!

Moreover, I use TypeScript to that code for a better developer experience. The last thing that deserves to mention is the render page content function that receives the route data and renders an appropriate component.

It's possible to do the same using the switch statement, but I wanted to do that more declaratively.

In the GraphQL examples above, I showed you how to fetch product details, category data, and CMS pages. Components rendered by renderPageContent are perfect places to display that information. They receive the data as a prop, and then its responsibility is to say information on the screen.

---

## Conclusion

This article showed you basic concepts about routing in headless apps connected with Magento GraphQL API.

There is the route query that resolves the URL and returns one of three page types: CMS_PAGE, Category, and Product. You can render those pages using one dynamic route on the front-end side.

You can create static routes for other pages like checkout or my account add implementation.

Thanks to state-of-the-art features like React Server Components, you can do all of that on the server-side, so the performance of a page will be outstanding.

#WebDevelopment #BackendDevelopment #FrontendDevelopment #JavaScript #TypeScript #GraphQL #React #NextJS #Magento #ConceptExplanation #Tutorial #DeepDive #Intermediate #API #Routing #Headless #SEO
