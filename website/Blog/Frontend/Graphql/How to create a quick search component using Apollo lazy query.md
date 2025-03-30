*Published at 29/09/2022*

When React renders a component that calls the **useQuery** hook, the Apollo Client runs the query automatically, but sometimes you need to query for data on some event. A great case is a quick search component that allows users to search for products in an eCommerce store.

There is a **useLazyQuery** hook that returns a query function. You can use this function wherever you want, and when you fire it, Apollo will execute a query for you.

## When would you use lazy queries?

Typically custom Apollo's hook **useQuery** is used when you want to query data. That kook is called when React mounts and renders the component, and Apollo Client automatically executes a query then.

What to do when you want to call a query manually thought? For instance, when a user clicks on a specific button, or if you're running a query in a **useEffect** function?

### Lazy queries for the rescue

In that case, you can use the **useLazyQuery hook**. As I mentioned earlier, It's pretty much the same as useQuery with one exception. When **useLazyQuery** is called, it does not immediately execute its associated query.

Instead, it returns a function in its result tuple that you can call whenever you're ready to execute the query.

On the other hand, the useLazyQuery hook is ideal for executing queries in response to different events, such as user actions. Whenever the useLazyQuery command occurs, the application will not immediately run any queries. You need to trigger a query **manually**.

### Take a look at the example

```javascript
import React from "react";
import { useLazyQuery } from "@apollo/client";
import { GET_SWEETIES } from "./somewhere";

const MySweeties = () => {
  const [getSweeties, { loading, data }] = useLazyQuery(GET_SWEETIES);

  if (loading) return <p>Loading ...</p>;

  const shouldDisplaySweeties =
    data && data.sweeties ? (
      <img src={data.sweeties.image} alt="sweeties" />
    ) : (
      <button onClick={() => getSweeties({ variables: { type: "chocolate" } })}>
            Get sweeties!   
      </button>
    );

  return shouldDisplaySweeties;
};
```

How useful is that?

## Refetch function

The **useQuery** returns data, and the **useLazyQuery** returns data as well. Those hooks return cached data or server data. It doesn't matter, they return the requested data and the component renders that data. The default behavior of the useQuery hook is to perform a query when the component re renders. Lazy query allows performing a query on demand.

Moreover, an additional mechanism allows to **refetch** queries on demand to particular **user action**. Take a look at the example:

```javascript
const { loading, error, data, refetch } = useQuery(YOUR_QERY, {
  variables: { sampleVar: "abc" },
});
```

You can bind refetch function in the JSX code like this:

```javascript
<button onClick={() => refetch({ sampleVar: "xyz" })}>Refetch</button>
```

As you can see, you can pass new variables to the function.

## Practical usage

Let's use that knowledge about lazy queries and implement a QuickSearch component in the React app.

### QuickSearch component

Create a quick search component with the following content:

```javascript
import React, { useState } from "react";
import { Form, FormControl } from "react-bootstrap";
import QuickSearchSuggestions from "../QuickSearchSuggestions";

const QuickSearch = () => {
  const [isValid, setIsValid] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const handleChange = (value) => {
    const valueEntered = !!value;
    const isValid = valueEntered && value.length > 3;

    setIsValid(isValid);
    setSearchQuery(value);
  };

  return (
    <div className="justify-content-center d-flex position-relative">
                  
      <Form inline className="w-100">
                        
        <FormControl
          type="text"
          placeholder="Search entire shop"
          className="w-100"
          onChange={(e) => handleChange(e.target.value)}
        />
                    
      </Form>
                  
      <QuickSearchSuggestions isValid={isValid} searchQuery={searchQuery} />
              
    </div>
  );
};

export default QuickSearch;
```

I define two states there: isValid and searchQuery, and I pass them to the child component. I check the length of the value entered by a user in the search input, and if the length is higher than 3, I send the query.

### Quick Search Suggestion component

Create a new component called **QuickSearchSuggestion** with the following content:

```javascript
import React from "react";

import { ListGroup } from "react-bootstrap";
import PropTypes from "prop-types";
import useQuickSearchSuggestions from "../../hooks/useQuickSearchSuggestions";
import classes from "./QuickSearchSuggestions.module.css";

const QuickSearchSuggestions = (props) => {
  const { isValid, searchQuery } = props;
  const { hasSuggestions, isLoading, isOpen, items } =
    useQuickSearchSuggestions({ isValid, searchQuery });

  const suggestions = items.map((product) => {
    return (
      <ListGroup.Item key={product.id}>
                    {product.name}
                
      </ListGroup.Item>
    );
  });

  const shouldDisplaySuggestions = suggestions ? (
    <div className={classes.suggestions}>
              
      <ListGroup>
                    {suggestions}
                
      </ListGroup>
          
    </div>
  ) : null;

  if (isOpen && hasSuggestions) {
    return shouldDisplaySuggestions;
  } else if (isLoading) {
    return (
      <div className={classes.suggestions}>
                    <ListGroup.Item>Loading...</ListGroup.Item>
                
      </div>
    );
  } else if (isOpen && !hasSuggestions) {
    return (
      <div className={classes.suggestions}>
                    
        <ListGroup>
                          <ListGroup.Item>No products found</ListGroup.Item>
                      
        </ListGroup>
                
      </div>
    );
  } else {
    return null;
  }
};

QuickSearchSuggestions.propTypes = {
  isValid: PropTypes.bool.isRequired,
  searchQuery: PropTypes.string.isRequired,
};

export default QuickSearchSuggestions;
```

I use a custom hook there: **useQuickSearchSuggestion**. That hook's responsibility is to provide data and business logic for the component. I am going to define that hook in the next step.

To finish the QuickSearchSuggestion, I create a CSS module **QuickSearchSuggestions.module.cs**s with the following styles:

```
.suggestions {
    left: 0;
    position: absolute;
    top: 100%;
    right: 0;
    z-index: 10;
}
```

### use Quick Search Suggestions custom hook

```javascript
import { useEffect, useState } from "react";
import { useLazyQuery } from "@apollo/client";
import { GET_QUICK_SEARCH_SUGGESTIONS } from "../../queries/product.gql";
/**
 * The useQuickSearchSuggestions hook provides data and business logic for the QuickSearchSuggestions component
 *
 * @return {
 *  hasSuggestions {bool} - determines are products found based on provided search query
 *  isLoading {bool} - determines is data is currently loading
 *  isOpen {bool} - determines is component is opened
 *  items {array} - array with products returned from the API based on provided search query
 * }
 */
export const useQuickSearchSuggestions = (props) => {
  const { isValid, searchQuery } = props;
  const [isOpen, setIsOpen] = useState(false);
  const [hasSuggestions, setHasSuggestions] = useState(false);
  const [fetchSuggestions, { loading, data }] = useLazyQuery(
    GET_QUICK_SEARCH_SUGGESTIONS,
  );

  useEffect(() => {
    if (isValid) {
      fetchSuggestions({
        variables: {
          searchQuery,
        },
      });
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }
  }, [fetchSuggestions, isValid, searchQuery]);

  useEffect(() => {
    data && data.products && data.products.items && data.products.items.length
      ? setHasSuggestions(true)
      : setHasSuggestions(false);
  }, [data]);

  return {
    hasSuggestions,
    isLoading: loading,
    isOpen,
    items:
      data && data.products && data.products.items ? data.products.items : [],
  };
};

export default useQuickSearchSuggestions;
```

As you can see, I've defined a lazy query that returns the **fetchSuggestions** function.

Then I use that function in effect. Before calling, I check if the search query is valid and update the isOpen flag. The fetchSugestions query function takes **graphql** variables (searchQuery), fetch the data, and returns it to the react component.

### graphQL query

The last thing we need to do is create a [[The full-stack guide to the GraphQL query|graphQl query]] used by the useQuickSearchSuggestions hook.

```javascript
export const GET_QUICK_SEARCH_SUGGESTIONS = gql`
    query getQuickSearchSuggestions($searchQuery: String!) {
        products(search: $searchQuery) {
            items {
                id
                name
                small_image {
                    url
                }
                url_key
                url_suffix
                price {
                    regularPrice {
                        amount {
                            value
                            currency
                        }
                    }
                }
            }
        }
    }
`;
```

---

## Summary

It looks like the Quick Search functionality works good:

So to execute GraphQL queries using **Apollo GraphQL** client, you can choose between two custom apollo react hooks:

1. useQuery

2. useLazyQuery

### What is the difference between useQuery hook and useLazyQuery?

When using useLazyQuery, it does not perform the associated query. Instead, the function returns query functions in the result tuples called when the query is executed.

The useLazyQery hook is perfect when you, for example, need to fetch data for the GraphQL server on user action, user clicking, or typing.

### Apollo React Hooks and cached data

Apollo client provides a cache mechanism called InMemoryCache. Thanks to that, the apollo cache query results in memory. Of course, Apollo react hooks supports that cache. You can set the default fetch policy globally and locally on each query.

### Handling [GraphQL](/how-to-use-graphql-mutations-in-react-and-apollo-client) errors

Lazy query error handling is pretty the same as when you use the **useQuery** hook. Please follow [[2 ways of handling GraphQL errors in Apollo Client|this article]] if you want to get more about GraphQL errors.
