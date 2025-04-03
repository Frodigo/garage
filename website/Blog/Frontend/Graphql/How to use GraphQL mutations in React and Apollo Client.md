---
date: 2022-10-27
title: How to use GraphQL mutations in React and Apollo Client
---
*Last updated: 27/10/2022*

In one of my previous articles, I described [[The full-stack guide to the GraphQL query|[GraphQL queries]]. Today I would like to show you how to work with GraphQL mutations.

## What is a mutation in GraphQL?

A mutation is a function that allows you to modify data. In REST APIs, data is typically fetched by the GET method and added or modified by the POST or PUT method.

In GraphQL, there are two types of operations:

1. Query: fetching data

2. Mutation: modifying/adding data

## Mutation example

Take a look at the simple mutation from the Magento eCommerce platform's GraphQL API that creates an empty cart:

```javascript
mutation {
  createEmptyCart(input: {})
}
```

Mutation receives an empty input object and returns a token of the newly created cart.

Let's try something more complicated - a mutation that takes some input via variables:

```javascript

mutation {
  addSimpleProductsToCart(input: { cart_id: "B06YCRcXAaOHGTtZ2Iij8SDHAq0AR49F", cart_items: [{ data:{sku: "24-MB01", quantity: 1} }] }) {
    cart {
      total_quantity
      items {
        product {
          name
        }
      }
    }
  }
}
```

In this example, you can see the addSimpleProductsToCart mutation that takes an input object with the following variables:

- **cart_id**: Cart ID to which the product will be added

- **cart_items**: array of objects that contains the SKU of the product and its quantity. The example above adds one product of SKU *24-MB0_1 to the cart with ID _B06YCRcXAaOHGTtZ2Iij8SDHAq0AR49F*

Mutation returns the cart object, and in this example, I requested total_quantity of the cart and information about the cart items' names.

The response to that GraphQL mutation looks like this:

```javascript
{
  "data": {
    "addSimpleProductsToCart": {
      "cart": {
        "total_quantity": 1,
        "items": [
          {
            "product": {
              "name": "Joust Duffle Bag"
            }
          }
        ]
      }
    }
  }
}
```

Hard-coding variables is not a good idea in real projects, so take a look at an example where I pass variables by arguments:

```javascript
mutation addSimpleProductsToCart($input: AddSimpleProductsToCartInput ) {
  addSimpleProductsToCart(input: $input) {
    cart {
      total_quantity
      items {
        product {
          name
        }
      }
    }
  }
}
```

In this case, you can pass variables as an object:

```javascript
{
  "input": {
    "cart_id": "B06YCRcXAaOHGTtZ2Iij8SDHAq0AR49F",
    "cart_items": [
      {
        "data": {
          "sku": "24-MB01",
          "quantity": 1
        }
      }
    ]
  }
}
```

---

## Apollo Client

Apollo Client is one of the most popular GraphQL clients for React, and in this article, I want to show you how to work with mutations using Apollo Client and React.

### Prerequisites

If you want to run the examples below on your computer, you should:

1. Set app a new React App using [create-react-app](https://create-react-app.dev/docs/getting-started)

2. [Initialize Apollo Client](https://www.apollographql.com/docs/react/get-started/) (note: I used Magento GraphQL API in examples, but it is up to you which API you would like to use)

## Execute mutation in Apollo client

Apollo Client offers predefined hooks to execute GraphQL queries and mutations. These hooks offer much more than only sending requests and receiving responses. Let's go dive to see what the useMutation hook provides.

### The useMutation hook

Let's see how the **useMutation** hook works with a real example*.* To do so, I use the createEmptyCart mutation. First, I need to define that mutation in the code:

```javascript
import { gql, useMutation } from "@apollo/client";

const CREATE_EMPTY_CART = gql`
  mutation {
    createEmptyCart(input: {})
  }
`;
```

That GraphQL operation takes no arguments so executing is very simple and looks like this:

```javascript
useMutation(CREATE_EMPTY_CART);
```

Full example:

```javascript
import { gql, useMutation } from "@apollo/client";

const CREATE_EMPTY_CART = gql`
  mutation {
    createEmptyCart(input: {})
  }
`;

function App() {
  const [mutateFunction, { data, loading, error, called, reset }] =
    useMutation(CREATE_EMPTY_CART);

  if (loading) {
    return <>Loading...</>;
  }

  return (
    <main style={{ padding: "10px" }}>
      <h1>GraphQL mutations tutorial</h1>
      <button type="button" onClick={() => mutateFunction()}>
        Create cart
      </button>

      <div>
        <h2>Data: </h2>
        {data && data.createEmptyCart}
      </div>
      {error && (
        <div>
          <h2>Error:</h2>
          {error.toString()}
        </div>
      )}
      <div>
        <h2>Called: {called.toString()}</h2>
        <button type="button" onClick={() => reset()}>
          Reset
        </button>
      </div>
    </main>
  );
}

export default App;
```

This part of the code:

```javascript
const [mutateFunction, { data, loading, error }] = useMutation(CREATE_EMPTY_CART);
```

Is responsible for initializing the useMutation hook in the component

### Mutation response

The useMutation hook returns an array that contains mutate function and an object with some properties.

#### mutate Function

A function that must be called to execute mutation. This example is named as mutateFunction, but you can name it what you want for example, you can use the operation name: createEmptyCart, or whatever you want.

The code below is responsible for executing mutation:

```javascript
<button type="button" onClick={() => mutateFunction()}>Create cart</button>
```

Basically, there is a button that has bounded the mutate function on the click event. So when the user clicks that button, the mutation will be executed.

#### data

The data fields contain the mutation response. Then you can use this data in the component. In this example, I display the mutation response on the screen:

```html
<div>
  <h2>Data:</h2>
  {data && data.createEmptyCart}
</div>
```

#### LOADING

The loading fields show the state of the mutation. If it's true, that means that mutation is in progress and fetches data at the moment. When mutation returns value and execution is finished, the loading field equals false.

In this example, I use the loading field only to display the loading information on the screen:

```javascript
if (loading) {
  return <>Loading...</>;
}
```

#### error

When mutation meets some errors on the backend side, they will be returned here. The error object can contain either an array of **graphQLErrors** objects or one single **networkError** object. If GraphQL server doesn't produce any error, the error object is **undefined**.

In my example, I display potential errors on the screen:

```javascript
{
  error && (
    <div>
      <h2>Error:</h2>
      {error.toString()}
    </div>
  );
}
```

#### called

The **called** is a flag that describes if mutate function is called or not.

#### Reset

When you want to rest the mutation state to initial, you call the reset() function. That means Apolo will restore all fields returned by the useMutation hook. to default values.

### Mutation options

The previous example was straightforward. I didn't even pass any variables there. Let's see something more sophisticated. To pass additional parameters to the useMutation hook, you must pass an object as a second argument to the operation.

```javascript
const [mutateFunction, { data, loading, error, called, reset }] = useMutation(
  MUTATION_STRING,
  {
    // additional options here
  },
);
```

Note: MUTATION_STRING is a GraphQL query string parsed with the **gql** template literal.

#### Variables

The variables object allows passing GraphQL variables to the mutation. Each key in this object represents one variable.

```javascript
const CREATE_EMPTY_CART = gql`
   mutation createCart($input: createEmptyCartInput) {
    createEmptyCart(input: $input)
  }
`;

function App() {
  const [mutateFunction, { data, loading, error, called, reset }] = useMutation(CREATE_EMPTY_CART, {
    variables: {
      input: {
        cart_id: 'lTO8UjTglq5djnpIOseLN7RWvpvwSRba'
      }
    }
  });

 (...) // rest of the code
```

I updated the mutation string, and from now it accepts one argument: $input object:

```javascript
mutation createCart($input: createEmptyCartInput) {
    createEmptyCart(input: $input)
}
```

Then I passed the variables object to the useMutation hook:

```javascript
const [mutateFunction, { data, loading, error, called, reset }] = useMutation(
  CREATE_EMPTY_CART,
  {
    variables: {
      input: {
        cart_id: "lTO8UjTglq5djnpIOseLN7RWvpvwSRba",
      },
    },
  },
);
```

#### errorPolicy

The errorPolicy field allows specifying how the hook handles errors.

Possible values:

- **None** (default value) - if the response contains errors, they are returned on the error object, and data is undefined.

- **Ignore** \- errors are skipped, so the error object is not populated even if something goes wrong.

- **All** - two objects: data and error, are populated. This is useful if you want to settle partial data even if something went wrong during the mutation execution.

#### onCompleted

The onCompleted is a callback function called when the mutation was executed without errors. In this function, you can access mutation results and options passed to the mutation. Take a look at the example:

```javascript
import { gql, useMutation } from "@apollo/client";

const ADD_PRODUCT_TO_CART = gql`
  mutation AddProductsToCart($cartId: String!, $cartItems: [CartItemInput!]!) {
    addProductsToCart(cartId: $cartId, cartItems: $cartItems) {
      cart {
        id
        items {
          quantity
          prices {
            row_total {
              currency
              value
            }
          }
        }
        prices {
          grand_total {
            currency
            value
          }
        }
        total_quantity
      }
    }
  }
`;

const [addProductToCart] = useMutation(ADD_PRODUCT_TO_CART, {
  variables: {
    cartId: "koESgYi6WU5BiCJDRkgfilDB4z1IsfHV",
    cartItems: [
      {
        selected_options: ["Y29uZmlndXJhYmxlLzE0NC8yMTU"],
        quantity: 1,
        sku: "GC-747-SOCK",
      },
    ],
  },
  onCompleted: (data, options) => {
    console.log(data, options);
  },
});

// (...)
<button type="button" onClick={() => addProductToCart()}>
  Add product to cart
</button>;
```

#### onError

The onError is a callback function called when a mutation returns some error. In this function, you can access the error object and options passed to the mutation.

### Updating the cache

Apollo client has its own caching system and, by default, writes data to the cache. The cache impacts the speed of operation, because some operations can retrieve data only from the cache or first from the cache and then from the server.

In addition, a technique called optimistic responses can be used in working with mutations. Let me explain this to you with an example:

1. The user enters the website

2. Apollo downloads a list of products and displays them on the screen

3. The user adds a product to the basket

4. Storefront needs to update the shopping cart details.

After executing the mutation, we have two to accomplish this:

1. Update the cart data in the cache

2. Perform the shopping cart inquiry again

Let's see how to implement this in Apollo.

#### How Apollo Updates the cache

First, let's create a new query that fetches the cart:

```javascript
const GET_CART = gql`
  query getCart {
    cart(cart_id: "koESgYi6WU5BiCJDRkgfilDB4z1IsfHV") {
      id
      items {
        quantity
        prices {
          row_total {
            currency
            value
          }
        }
      }
      prices {
        grand_total {
          currency
          value
        }
      }
      total_quantity
    }
  }
`;
```

Second, use the useLazyQuery hook to execute the query:

```javascript
const [getCart] = useLazyQuery(GET_CART, {
  onCompleted: (data) => {
    console.log("cart data: ", data);
  },
});
```

Third, add a button and bind the getCart function to the onClick event of that button:

```javascript
<button type="button" onClick={() => getCart()}>
  Get cart
</button>
```

When the user clicks that button, the query is executed and the onCompleted callback prints cart data to the console.

At the same time, Apollo writes data of that cart to the cache.

Now, when the user clicks Add Product to cart button, Apollo runs the addProductToCart mutation, and the product will be added to the cart on the server side. Under the hood, Apollo updates the cart data in the cache.

##### Updating cache manually

In some cases, Apollo is not able to update the cache automatically. Then you can define your own update function and write to the cache manually. You can pass an update function as a field of the settings object that useMutation hook receives:

```javascript
import { gql, useMutation } from "@apollo/client";

const [addProductToCart] = useMutation(ADD_PRODUCT_TO_CART, {
  // (...)
  update(cache, { data: { addProductsToCart } }) {
    cache.modify({
      fields: {
        cart(existingCartRef = {}) {
          const newCartRef = cache.writeFragment({
            data: addProductsToCart.cart,
            fragment: gql`
              fragment NewCart on Cart {
                id
                items {
                  quantity
                  prices {
                    row_total {
                      currency
                      value
                    }
                  }
                }
                prices {
                  grand_total {
                    currency
                    value
                  }
                }
                total_quantity
              }
            `,
          });
          return { ...existingCartRef, newCartRef };
        },
      },
    });
  },
});
```

The update function receives the cache object and data returned by the mutation.

On the cache object, there is the modify function that allows updating the cache. In that function, I create a new cart fragment that contains data returned from mutation, and at the end, I return the merged cache cart with a new cart. Then Apollo updates the cache.

#### refetchQueries

Another mechanism to update the state after mutation execution is refetching queries. You can specify which queries should be executed by passing them to the refetchQueries array.

```javascript
const [addProductToCart] = useMutation(ADD_PRODUCT_TO_CART, {
  // (...)
  refetchQueries: ["getCart"],
});
```

the "getCart" is the query defined earlier:

```javascript
const GET_CART = gql`
  query getCart {
     // (...)
  }
`;
```

Alternatively, you can pass the query as an object like this:

```javascript
const GET_CART = gql`
  query getCart {
     // (...)
  }
`;

// (...)

const [addProductToCart] = useMutation(ADD_PRODUCT_TO_CART, {
  // (...)
  refetchQueries: [{ query: GET_CART }],
});
```

### Optimistic responses

When you perform graphql mutations, they modify server-side data, which can take some time. You would have new data as fast as possible and display it to the user. Apollo provides an interesting mechanism: **Optimistic mutation results**, and thanks to this feature, you can update your UI before your server responds. Take a look at how it works:

```javascript
const [addProductToCart] = useMutation(ADD_PRODUCT_TO_CART, {
  // (...)
  optimisticResponse: {
    addProductsToCart: {
      cart: {
        id: "koESgYi6WU5BiCJDRkgfilDB4z1IsfHV",
        __typename: "Cart",
        total_quantity: 40,
        // other cart fields
      },
    },
  },
});
```

The optimisticResponse object takes an object with the same structure as the expected mutation response. When the mutate function is called, UI will be updated. Finally, when a request is done, Apollo replaces the fake data you specified with real server side data.

---

## Conclusion

Mutations next to queries are the core of Apollo Client's API. Sending a request and receiving a response is not all that Apollo Client offers. Thanks to the fact that Apollo has its state, developers can reliably program communication with the API and provide users with a very good UX. One of the most interesting features is optimistic responses, thanks to which the UI will seem fast even when the server is slow.

#WebDevelopment #FrontendDevelopment #BackendDevelopment #JavaScript #React #GraphQL #ApolloClient #REST #ConceptExplanation #Tutorial #DeepDive #Intermediate #DataPipeline #PerformanceOptimization