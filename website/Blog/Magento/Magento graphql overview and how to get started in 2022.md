*date: 14/04/2022*

**GraphQL** has become one of the most popular APIs for building web applications. It gives many benefits for frontend development:

- query language and the possibility to get precisely that data from the backend that you need

- one endpoint for everything

- self-documented API operations

- validation out-of-the-box

**Magento 2** has supported GraphQL for a while, and in the case of creating a headless storefront, GraphQL API is a perfect choice. I want to show you the benefits of using GraphQL API and how to work with it, and at the end, I will show you some example queries that fetch some basic eCommerce stuff like categories, products, cms pages, and carts.

---

## Magento 2 API: What's new?

The main problem with GraphQL in Magento when it was introduced that developers met was the lack of supported Magento features. Magento itself has a massive amount of fantastic features, and it's essential to have as many of them as possible supported in API. Of course, it's an option to use REST API in some places instead of GraphQL, but it is not a perfect solution.

Anyway, Adobe and Magento community have been working hard to improve and develop Magento GQL API. **They have recently added many new supported features related to a customer, my account, and b2b functionalities.**

On the other hand, module vendors started providing custom GraphQL queries and notations as a part of the custom GraphQL module. In case when an extension does not has GraphQL support, implementing GraphQL operations is still an option because Magento 2 API is extensible.

---

## GraphQL compared to REST API

I won't elaborate on the difference between GraphQL API and REST API (or even with soap API) because there are many great articles about that on the web. Still, I want to focus on GraphQL benefits from a frontend perspective. Read the below paragraphs to see more details.

### Query language and Graphql schema

When you want to fetch some data from GraphQL API, you basically need to specify what data you need. To do so, you inspect the GraphQL schema and choose what you will query about.

For example, in Magento, there is a **categoryList** GraphQL query that returns an array containing information about the category. There are a lot of fields, and depending on the situation and your needs, you select whatever you want, for example, UID of category and name:

```javascript
query getCategories(
    $filters: CategoryFilterInput,
  ) {
    categoryList(filters: $filters) {
      uid
      name
  }
}

// variables passed to the query:

{
  "filters": {
    "url_path": {
      "eq": "gear/bags"
    }
  }
}

// results:
{
  "data": {
    "categoryList": [
      {
        "uid": "NA==",
        "name": "Bags"
      }
    ]
  }
}
```

Here you can see the schema definition for the categoryList query:

Of course, there are more fields, but they are out of the screenshot, sorry 😆

---

### One endpoint

The next advantage of GraphQL is one endpoint for all requests. In REST API, each request has a different URL, and in addition, each URL can have multiple behaviors depending on the **HTTP** method like **POST**, **GET**, **PUT**, and so on.

GraphQL haters can say that it's not a problem. I agree it's not a problem, but let's explain that to frontend developers 😂

Using GraphQL is relatively easier for frontend developers than using REST API because everything is in one place, in one endpoint and even calling API is simpler because you have to change only the payload you send to API.

### Multiple resources at the same time

In REST API, when you want to fetch multiple resources, for example, categories and products, you need to send requests to various endpoints. This complicates implementation and decreases performance because each millisecond count and each HTTP request increase communication time with APIs in the Core Web Vitals world.

Using GraphQL, you can fetch multiple resources in one query, so it's not a problem to fetch products and categories simultaneously, and it's not even a problem to fetch a cart as well.

### Validation

GQL provides schema validation OOTB, so if you send a wrong request, you miss some variables, and you will see meaningful errors. For example, if you query for a field that doesn't exist, [GraphQL](https://marcin-kwiatkowski.com/blog/graphql/2-ways-of-handling-graphql-errors-in-apollo-client) will inform you that the field you requested does not exist.

### No more over-fetching

REST API typically returns a wall of data, and in most cases, 98% of data returned from REST API is redundant on the front. This dramatically increases the size of HTTP calls and decreases performance.

Well designed application that consumes GraphQL API fetches only that data that is needed in UI, so you get what you need, and the size of API calls is smaller

---

## How to connect with Magento2 GraphQL API

To connect with Magento 2 GraphQL API, you must send a request to the GraphQL endpoint. Typically is **https://<magento_base_url>/graphql.**

You can use some of the GraphQL playgrounds or browsers extensions to test GraphQL API and send some queries and mutations. I use [Altair GraphQL Client Google](https://chrome.google.com/webstore/detail/altair-graphql-client/flnheeellpciglgpaodhkhmapeljopja?hl=en) chrome extension

Extensions like that are compelling and allow you to send graphql queries, mutations, set variables, HTTP headers, and read schema documentation so testing each GraphQL API is easy.

---

## Magento GraphQL endpoint HTTP headers

There is one crucial thing about sending GraphQL requests: the possibility of changing the response by adding specific HTTP headers.

### Magento 2 GraphQL API and Multistore

When you have configured Multistore in the Magento backend, you can fetch data for different store views by passing the **Store** HTTP header.

Imagine that you have two store views: default and german, and those store views have set up different languages: English for the default store view and german for the german store. If you wanted to send a query for categories, you would have to use a graphQL query like this:

```javascript
{
  categoryList {
      uid
      name
      url_key
      children {
        uid
        name
        url_key
      }
  }
}
```

The possible response can look like this:

```json
{
  "data": {
    "categoryList": [
      {
        "uid": "Mg==",
        "name": "Default Category",
        "url_key": null,
        "children": [
          {
            "uid": "Mzg=",
            "name": "What's New",
            "url_key": "what-is-new"
          },
          {
            "uid": "MjA=",
            "name": "Women",
            "url_key": "women"
          },
          {
            "uid": "MTE=",
            "name": "Men",
            "url_key": "men"
          },
          {
            "uid": "Mw==",
            "name": "Gear",
            "url_key": "gear"
          },
          {
            "uid": "OQ==",
            "name": "Training",
            "url_key": "training"
          },
          {
            "uid": "Mzc=",
            "name": "Sale",
            "url_key": "sale"
          }
        ]
      }
    ]
  }
}
```

![](/images/blog/6cc1889f-d304-4353-9e39-1152ec198808-1024x633.png)

Assuming you have translated category names for the german store, you have just to set Store header equals 'german' to fetch categories for the german store. You would see categories for a german store below.

```json
{
  "data": {
    "categoryList": [
      {
        "uid": "Mg==",
        "name": "Default Category",
        "url_key": null,
        "children": [
          {
            "uid": "Mzg=",
            "name": "Was gibt's Neues",
            "url_key": "what-is-new"
          },
          {
            "uid": "MjA=",
            "name": "Frau",
            "url_key": "women"
          },
          {
            "uid": "MTE=",
            "name": "Männer",
            "url_key": "men"
          },
          {
            "uid": "Mw==",
            "name": "Ausrüstung",
            "url_key": "gear"
          },
          {
            "uid": "OQ==",
            "name": "Ausbildung",
            "url_key": "training"
          },
          {
            "uid": "Mzc=",
            "name": "Sale",
            "url_key": "sale"
          }
        ]
      }
    ]
  }
}
```

Remember that the query is the same so passing a Store header to requests allows you to fetch data for different stores. Magento multistore is mighty to have different categories, products, prices, languages, and cms content for different store views.

### Graphql queries in Magento and currency

Price and currency are an essential part of each eCommerce platform because the product has prices, brands typically operate in different markets and different countries, and allow to buy products in other currencies. Luckily, GraphQL in Magento will enable you to fetch different prices for different stores with different currencies.

---

#### Fetch available currencies data from Magento 2

You can set available currencies for each store view in the Magento backend panel. To do so, log in as an administrator and go to **Stores -> Configuration -> General -> Currency Setup.** There you can see **Allowed Currencies** multi-select. When you uncheck the "**Use system value**" checkbox, you will be able to select available currencies for the selected store view.

The next step is to fetch those currencies to display the currencies switcher on the storefront.

To do that, use the currency graphql query:

```json
{
  currency {
        available_currency_codes
    }
}
```

In my demo store it returns these results:

```json
{
  "data": {
    "currency": {
      "available_currency_codes": ["EUR", "PLN", "USD"]
    }
  }
}
```

When you need to fetch available currencies for other store views, you must again set the **Store** HTTP header (as in the example with categories that I have shown you earlier).

---

#### Fetch correct prices for the selected currency

Based on available currencies data, it's easy to implement a currency switcher on a storefront and add the possibility for customers to select a currency. When customers choose a different currency than the default one, we have to send that information to Magento.

There is the **Content-Currency** HTTP header, and if it's passed to the GraphQL endpoint, Magento will return prices in the specified currency. For example, let's fetch some products from Magento:

```javascript
query getProductsForCategory(
    $filter: ProductAttributeFilterInput,
  $productsPageSize: Int = 10,
   $currentProductsPage: Int = 1
  ) {
    products(filter: $filter, pageSize: $productsPageSize, currentPage: $currentProductsPage) {
      items {
        uid
        name
        price_range {
          maximum_price {
            final_price {
              currency
              value
            }
            regular_price {
              currency
              value
            }
          }
          minimum_price {
            final_price {
              currency
              value
            }
            regular_price {
              currency
              value
            }
          }
        }
      }
  }
}
```

Let's fetch just one product for one of the categories. I want to use the Bags category that has **UID** equals **NA==**. Variables that I pass to query look like this:

```json
// variables
{
  "filter": {
    "category_uid": {
      "eq": "NA=="
    }
  },
  "productsPageSize": 1
}
```

For that query and variables, Magento returns this data for me:

```json
{
  "data": {
    "products": {
      "items": [
        {
          "uid": "MTQ=",
          "name": "Push It Messenger Bag",
          "price_range": {
            "maximum_price": {
              "final_price": {
                "currency": "USD",
                "value": 45
              },
              "regular_price": {
                "currency": "USD",
                "value": 45
              }
            },
            "minimum_price": {
              "final_price": {
                "currency": "USD",
                "value": 45
              },
              "regular_price": {
                "currency": "USD",
                "value": 45
              }
            }
          }
        }
      ]
    }
  }
}
```

As you can see, the returned currency is **USD** (because it is the default one), and prices are in USD. Now I set the **Content-Currency** HTTP header to **EUR, a**nd Magento will return prices in EUR. Take a look at the below code:

```json
{
  "data": {
    "products": {
      "items": [
        {
          "uid": "MTQ=",
          "name": "Push It Messenger Bag",
          "price_range": {
            "maximum_price": {
              "final_price": {
                "currency": "EUR",
                "value": 31.8
              },
              "regular_price": {
                "currency": "EUR",
                "value": 31.8
              }
            },
            "minimum_price": {
              "final_price": {
                "currency": "EUR",
                "value": 31.8
              },
              "regular_price": {
                "currency": "EUR",
                "value": 31.8
              }
            }
          }
        }
      ]
    }
  }
}
```

### Authorization with Magento 2 GraphQL

Another crucial thing relates to HTTP headers is Authorization. When you want to fetch content available only for logged-in users, like customer data, you must set the **Authorization HTTP header**. Then Magento will return that data. Otherwise, graphQL queries without that header will return validation notice that the customer isn't authorized to fetch data specified in a request.

---

## How to optimize Magento 2 GraphQL endpoint

Magento haters say that Magento GQL API is slow, but I must disagree with that. Maybe it is not the fastest on the market, but there are several options to optimize each request.

To optimize Graphql endpoints, I recommend using Varnish and changing the HTTP method for graphql queries from POST to GET. Then you can cache several queries and reduce the time of response twice or even more!

---

### Varnish caching example

Here you have the query that fetches 20 products from Magento without Varnish caching:

Response time is 311ms when response time with Varnish is only 96ms for the same query!

---

## Conclusion

Magento GQL is an API that allows you to fetch data from Magento using queries and save information in Magento using mutations. If you would experiment with Magento 2 GraphQL, you have to set up the Magento store or use one of the public available Magento demos, then use one of the GraphQL Clients or Chrome extensions like Altair GraphQL client. You can use Postman as well.

Magento 2 has excellent support in GraphQL API for its features and advantages compared to REST architecture. Hence, it's a perfect choice when you want to fetch required data in your headless storefront.

### GraphQL and headless

Nowadays, the most popular headless storefronts and boilerplates like Vue Storefront and PWA Studio use GraphQL API to communicate with Magento. Besides, Extensions providers for Magento 2 have started adding support for GraphQL in their extensions. That all can mean that headless storefronts, composable commerce, and all pretty new things will constantly be developing near future!
