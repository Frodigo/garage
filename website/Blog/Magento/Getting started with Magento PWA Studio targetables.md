*Published at: 04/10/2021*

As a Magento Frontend developer (If you are not deal with Magento, you can skip this paragraph), you have a few mechanisms to customize the look and feel of your shops, like Layout modifications, customizing styles, or creating mixins). These methods (if you can use their power) allows you to do whatever you want with your shop.

---

## Welcome to Magento PWA Studio

Magento PWA Studio was specially designed by the Adobe core team to help developers construct progressive web apps on Magento 2. This tool consists of ready-to-use, out-of-the-box solutions which are handy for headless storefronts development. The tool does have some benefits and weaknesses, including the value of the toolkits. In this article, I will show you one of the most powerful Magento PWA studio features: **the extensibility framework.**

---

## PWA Studio extensibility framework

PWA Studio has a built-in extensibility framework for developers to extends the new storefront based on the Venia concept easily. Before introducing this solution, developers were forced to overwrite files using the webpack plugin. Overwriting core files causes unexpected errors and complicates the project. Each overwrites complicates everything and is harder. Thanks to PWA studio extensibility Framework you can reduce overwriters as much as possible.

### Targetables

Regarding the [Magento](https://marcin-kwiatkowski.com/blog/pwastudio/what-is-the-difference-between-pwa-studio-and-the-current-magento-frontend) PWA, you also have a powerful mechanism for adding customizations called: targetables that allow you to modify the JSX output of your PWA (React) App during build-time. Targetables are part of the [pwa-buildpack](https://magento.github.io/pwa-studio/pwa-buildpack) module.

### Interceptor pattern

PWA Studio extensibility framework uses the Interceptor pattern to allow changes in PWA studio storefronts during code build time. That pattern allows you to modify code in a way that Magento PWA studio does know anything about that change. It means that you can enable/disable your piece of code and this is transparent for PWA Studio. Any changes in code are not necessary.

Take a look at how it works when you create a new project based on PWA Studio and want to add some changes there:

1. You scaffold a new project using pwa-buildpack CLI command-line instructions
2. You add a new module in the project directory, let's name it a @theme
3. You create an intercept file and put their instructions on which storefront parts you want to customize
4. You hook to specific targets that PWA Studio provides (I mean public API) to extend storefront by extensions/other modules
5. You use the public API provided by the pwa-buildpack module. For example, you use methods like **insertAfterJSX**, **removeJSX**, **setJSXprops**, and so on to achieve your goal
6. You can put all your extensions into one file, or have a few ones. Everything depends on you.
7. You run npm run build (or watch) and pwa-buildpack checks are there any interceptions exist and run those instructions.
8. If pwa-buildpack finds any error during build time, compilation fails, and errors are printed into the console.
9. Extensions are applied to the source code
10. Static code chunks contain modifications

### Note about targetables in PWA studio extensions

When you create your own extension you are able to add targets that other extensions can intercept. Because of security reasons PWA Studio restricts the scope of Targetable modifications in extensions. So you can add modifications only within the source code of extensions. That means in the case when you create and publish an npm package and someone wants to use your module, interceptors from the module won't work automatically. You can prepare a public function, and consumers will be able to use it in their local-intercept.js file and then your extension will affect a storefront.

---

## It's time to get your hands dirty

Enough of the theory. Let's see how it works in practice and create something using pwa-buildpack targetables!

Have you ever needed to add extra features to the Product Detail Page or wanted to customize it? I suppose the answer might be “yes” because the product page is probably the most frequently modified area in the online store.

In the following example, I would like to show you how to extend the product detail page into four steps:

- Get data from the API (define a [GraphQL](/the-full-stack-guide-to-the-graphql-query) query)

- Add Unit tests

- Create a component

- Inject the component to the Product Detail page

That process is repeatable for each customization you want to add to your store – however – in this article, we will work on a concrete case: how to add a short description to the product page.

---

## Prerequisites

1. **Scaffolded PWA Studio app** - if you don’t know how to set up PWA Studio on your local – check out my video tutorial:[https://youtu.be/lsiul60vBfs](https://youtu.be/lsiul60vBfs)

2. **Magento 2.4.2 installed locally** - theoretically, you can use the public Magento instance with Venia sample data installed, but you cannot change anything in the admin panel. For example, you cannot change a product’s short description, so it will be hard to test the code.

Let’s go ride code!

---

## Define a GraphQL query

The data comes from the Magento backend, and the only unknown thing is which GraphQL query we should use.

There is a products query:

```javascript
products(
   search: String
   filter: ProductAttributeFilterInput
   pageSize: Int = 20
   currentPage: Int = 1
   sort: ProductAttributeSortInput
): Products
```

The products query searches for products that match the criteria specified in the search and filter attributes.

We definitely want to get one specific product and to achieve that I’m wanna use a product SKU as a filter. When you take a look at **ProductAttributeFilterInput** (of filter argument) you will see that there is an SKU field that we can use:

```javascript
type ProductAttributeFilterInput {
    category_id: FilterEqualTypeInput
    category_uid: FilterEqualTypeInput
    description: FilterMatchTypeInput
    name: FilterMatchTypeInput
    price: FilterRangeTypeInput
    short_description: FilterMatchTypeInput
    sku: FilterEqualTypeInput
    url_key: FilterEqualTypeInput
}
```

---

### Note for GraphQL beginners

When you run your local PWA Studio instance, you will see an URL to the GraphQl playground. There you can find docs with all necessary information about GraphQL schema and possible information (like the information I Listed above)

Let’s define the query in **src / @theme / components / ShortDescription / ShortDescription.gql.js.**

```javascript
import gql from 'graphql-tag';

const GET_SHORT_DESCRIPTION_QUERY = gql`
    query shortDescriptionOfProduct($productSku: String!) {
        products(filter: { sku: { eq: $productSku } }) {
            items {
                uid
                short_description {
                    html
                }
            }
        }
    }


export default {
    queries: {
        getShortDescriptionQuery: GET_SHORT_DESCRIPTION_QUERY
    },
    mutations: {}
};
```

Of course, you can first use **GraphQL Playground** and write a query there, and when your query works as you want, you can just copy it to a source file in your project.

The query defined above takes one argument: product SKU, and it’s exported from the file as **queries.getShortDescriptionQuery.**

### Define unit tests

In our case, we just need to check two things:

1. It is a short description visible when a product has it set up

2. It is a short description invisible when a product does not have a short description filled. (in this case, we assume that component will return null)

Let’s create a file **src / @theme / components / ShortDescription / \_\_tests\_\_ / ShortDescription.spec.js** and add tests to it. Before we start, please add necessary imports:

```javascript
import React from "react";
import { render, getByText } from "@testing-library/react";
import { useQuery } from "@apollo/client";

import ShortDescription from "../ShortDescription";

jest.mock("@apollo/client");
```

### Note about dependencies

You can see I use [@testing-library/react](https://testing-library.com/docs/react-testing-library/intro/), so you need to add this as a dependency with other necessary dependencies. Also, you have to add config for jest to run tests. All of those things you can find in [this repository](https://github.com/Frodigo/tutorial-pwa-studio-short-description). Describing that process is out of the scope of this tutorial, but please reach out to me on Magento Community Slack if you have any questions.

### Memo about mocking

I mocked **@apollo/client** because I need to simulate communication with GraphQL API to test two scenarios I described earlier. Moreover, on the unit test level, we don’t want to test API.

I assumed that I would use the useQuery hook to fetch data from an API in my component.

### Test one: it renders component when the short description is filled in a product

```javascript
test("It renders component when the short description is filled in a product", () => {
  useQuery.mockReturnValue({
    data: {
      products: {
        items: [
          {
            uid: "1",
            short_description: {
              html: "<p>Lorem ipsum</p>",
            },
          },
        ],
      },
    },
  });

  const { container } = render(<ShortDescription productSku="abc" />);

  expect(getByText(container, "Lorem ipsum")).toBeDefined();
  expect(container).toMatchSnapshot();
});
```

I used **useQuery.mockReturnValue** function to define mocked returned value from API. Then I created an instance of ShortDescription component and passed “abc” value as the product SKU property (value is not essential here because returned data is mocked, so we need only to make sure that SKU is passed.

The next step is checking if Lorem ipsum text is rendered (defined). Take a look at the mock data - we returned the “lorem ipsum” paragraph there, so it should be rendered.

To check this, I used the **getByText** method of testing-library, which takes two arguments: container (tree, where we want to search, is passed value exists) and value (a value that we want to find in a specified container).

The function returns true if a value is defined in a container and false if not.

In the following line, we are just checking if rendered container matches the snapshot.

### Test two: it does not render when a product does not have the short description

```javascript
test("It does not render when a product does not have the short description", () => {
  useQuery.mockReturnValue({
    data: {
      products: {
        items: [
          {
            uid: "1",
            short_description: {
              html: "",
            },
          },
        ],
      },
    },
  });

  const { container } = render(<ShortDescription productSku="abc" />);

  expect(container.firstChild).toBeNull();
});
```

In the second case, there are two differences—the first one in another mocked data. The HTML field is empty.

The second one is to check that the rendered container is empty. I just check if container.firstChild is null.

---

## Create the component

We have already declared unity tests, and they, of course, fail because the component that we test is not defined yet. Let’s create it by adding a file **src / @theme / components / ShortDescription / ShortDescription.js** with following content:

```javascript
import React from "react";

import classes from "./ShortDescription.css";
import productOperations from "./ShortDescription.gql";

import { shape, string } from "prop-types";

const ShortDescription = (props) => {
  const { productSku } = props;
  const { queries } = productOperations;
  const { getShortDescriptionQuery } = queries;

  return <div className={classes.section}>Short description will be here</div>;
};

export default ShortDescription;

ShortDescription.propTypes = {
  classes: shape({
    root: string,
    section: string,
  }),
  productSku: string.isRequired,
};
```

From the beginning - we imported React because we want to create a React Component. Also, we imported a string checker from prop-types, and we use it to validate if productSku is passed:

```javascript
ShortDescription.propTypes = {
  productSku: string.isRequired,
};
```

The productOperations object is imported from the already declared **ShortDescription.gql.js** file.

The classes object is the CSS module with classes. We imported it from src / @theme / components /ShortDescription / ShortDescription.css. Let’s create that file.

```css
.root {
  margin: 15px 0;
}

.section {
  border-color: rgb(var(--venia-border));
  border-style: solid;
  border-width: 1px 0 1px;
  margin: 0 1.5rem;
  padding: 1.5rem 0;
}
```

Let’s back to the component file. You can see that we return static text:

```javascript
return <div className={classes.section}>Short description will be here</div>;
```

Let’s make it dynamic!

---

## Querying for data

The **getShortDescriptionQuery** is already imported, so now just import the useQuery hook from @apollo/client and use it to query data.

```javascript
import { useQuery } from '@apollo/client';
(..)
const ShortDescription = props => {
(...)
 const { data } = useQuery(getShortDescriptionQuery, {
          fetchPolicy: 'cache-and-network',
          variables: {
              productSku
          }
     });
(...)

};
```

Note: Because I want to keep this example simple, I do not handle errors here. If you would to take a look at how error handling can be done, [[2 ways of handling GraphQL errors in Apollo Client| check this article, please.]]

Now we can use data returned by the useQuery hook. For example: data.products.items\[0\].short_description.html, but this is not perfect.

### Save/memoize a short description

I have an idea: create a function that checks is a short description is defined and returns it. Otherwise return null.

I want to use the useMemo hook, which will memoize that value for us between re-renders of the component.

```javascript
const shortDescription = useMemo(() => {
  if (!data) return null;

  const { products } = data;

  if (
    products &&
    products.items &&
    products.items.length &&
    products.items[0].short_description &&
    products.items[0].short_description.html &&
    products.items[0].short_description.html.length
  ) {
    return products.items[0].short_description.html;
  }

  return null;
}, [data]);
```

The shortDescription field will be changed only when data (passed in dependency array - the second argument of the useMemo) is changed.

### Display short description

Let’s display a short description. Do you remember our test cases? If a description exists, we have to show it. Otherwise, we should return null.

Perfect, because our shortDescripotion constant has, in fact, two states: null or short description value.

We can use it to check what should be rendered. We will create the shouldRenderShortDescription constant that will yield a div contains a short description or return null.

BTW: the short description in the Magento backend is a WYSIWYG field, so the value returned from API is HTML. Let’s use the RichText component to render it:

```javascript
import RichText from '@magento/venia-ui/lib/components/RichText';
(..)
const ShortDescription = props => {
(...)
const shouldRenderShortDescription = shortDescription ? <div className={classes.root}>
        <div className={classes.section}>
            <RichText content={shortDescription} />
        </div>
    </div> : null;

    return shouldRenderShortDescription;

}
```

### Final component

Here is the finished source code of the ShortDesxcription component:

```javascript
import React, { useMemo } from "react";
import { useQuery } from "@apollo/client";
import RichText from "@magento/venia-ui/lib/components/RichText";

import classes from "./ShortDescription.css";
import productOperations from "./ShortDescription.gql";

import { shape, string } from "prop-types";

const ShortDescription = (props) => {
  const { productSku } = props;
  const { queries } = productOperations;
  const { getShortDescriptionQuery } = queries;

  const { data } = useQuery(getShortDescriptionQuery, {
    fetchPolicy: "cache-and-network",
    variables: {
      productSku,
    },
  });

  const shortDescription = useMemo(() => {
    if (!data) return null;

    const { products } = data;

    if (
      products &&
      products.items &&
      products.items.length &&
      products.items[0].short_description &&
      products.items[0].short_description.html &&
      products.items[0].short_description.html.length
    ) {
      return products.items[0].short_description.html;
    }

    return null;
  }, [data]);

  const shouldRenderShortDescription = shortDescription ? (
    <div className={classes.root}>
      <div className={classes.section}>
        <RichText content={shortDescription} />
      </div>
    </div>
  ) : null;

  return shouldRenderShortDescription;
};

export default ShortDescription;

ShortDescription.propTypes = {
  classes: shape({
    root: string,
    section: string,
  }),
  productSku: string.isRequired,
};
```

The last thing related to the component is to create an index.js file that will export it.

Create a file **src / @theme / components / ShortDescription / index.js**

```javascript
export { default } from "./ShortDescription";
```

---

## Inject the component to the PDP

We have good progress so far – the ShortDescription component is ready to use, unit tests have passed. Let’s inject the component to a product detail page using targetables.

### Add @theme dependency

Because of some unknown reasons, it’s not possible to use relative paths in the **local-intercept.js** file. The workaround for that is to create a virtual dependencyMagento using yarn link funcionality.

Add a new field to the “dependencies” array in PWA Studio root package.json:

```javascript
"@marcinkwiatkowski/theme": "link:src/@theme"
```

Run yarn install command. When the install process is done, you should see the **@marcinkwiatkowski/theme** package in node_modules. When you make changes in the **src/@theme** directory, they will automatically apply in **node_modules / @marcinkwiatkowski / theme** directory.

### Adding interceptor

Please replace local-intercept.js content with this one:

```javascript
const { Targetables } = require("@magento/pwa-buildpack");

module.exports = (targets) => {
  const targetables = Targetables.using(targets);
};
```

Now, we are ready to use targetables.

### Target the productFullDetail component

We want to add a short description between a title and quantity fields. After inspection, I figured out that the productFullDetail component is responsible for this area, so let’s handle it in the interceptor:

```javascript
(...)
const targetables = Targetables.using(targets);

const ProductDetailComponent = targetables.reactComponent(
    '@magento/venia-ui/lib/components/ProductFullDetail/productFullDetail'
);
```

### Import the ShortDescription component

Now we can add import to the productFullDetail component using targetables public API.

```javascript
const ShortDescription = ProductDetailComponent.addImport(
  "ShortDescription from '@marcinkwiatkowski/theme/components/ShortDescription'",
);
```

### Insert JSX

The last thing is to insert JSX in a specific place. Let’s add it after the section with class "title".

```javascript
(...)
ProductDetailComponent.insertAfterJSX('<section className={classes.title} />', `<${ShortDescription} productSku={productDetails.sku} />`)
```

The exciting thing here is passing props. I passed productDetails.sku. To understand it, let’s imagine when that line is executed, the scope of data is the same as in intercepted component.

That means you can use all values which exist in the intercepted component. In this case, we are intercepting the productFullDetail component, and the productDetails object is available there.

---

## Summary

I showed you the process of extending PWA Studio using targetables. We just used only one targetables method called insertAfterJSX, but there are a few more methods available.

Check out this article if you want to read more about targetables and other PWA Studio’s extensibility features.

---

## Source code

I pushed the source code of this tutorial to my GitHub. You can find it here: [https://github.com/Frodigo/tutorial-pwa-studio-short-description](https://github.com/Frodigo/tutorial-pwa-studio-short-description)

There you can find all source files and scaffolded Magento PWA studio project. Just clone the code, install dependencies by running the yarn install command in the project directory and run the storefront-project by yarn run watch command.
