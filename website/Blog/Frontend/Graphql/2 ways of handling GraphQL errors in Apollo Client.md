---
date: 2022-09-02
title: 2 ways of handling GraphQL errors in Apollo Client
---
If you use Graphql Apollo Client with React, there are two ways (more precisely speaking) – two levels of handling errors:

- operation level

- application level

## Operation-level errors handling

In this case, you have access to the **data**, **loading**, and **error** fields, and you can use an error object, which can be used to show a conditional error message.

```javascript
const { loading, error, data } = useQuery(YOUR_QUERY);

if (error) return <p>Error :(</p>;
```

Of course, you can create a component responsible for displaying errors in your app.

```javascript
import React from "react";
import PropTypes from "prop-types";

import classes from "./ErrorMessage.module.css";

const ErrorMessage = (props) => {
  const { error, ...rest } = props;

  const shouldDisplayError =
    error && error.message ? (
      <div className={classes.errorMessage} {...rest}>
        {error.message}
      </div>
    ) : null;
  return shouldDisplayError;
};

ErrorMessage.propTypes = {
  error: PropTypes.shape({
    message: PropTypes.string.isRequired,
  }),
};

export default ErrorMessage;
```

This component is really straightforward. It receives an error as a prop and displays that error to the user.

## Application-level error handling

Another approach is handling errors in Application-level. It allows you to create more complex logic.

Application-error handling lets you do whatever you want with errors. For example, you can log those errors to the console in **development** mode or use external tracking error tools like Sentry on **production**.

You can use this mechanism to display messages to the user as well. Let’s imagine that you have Messages Context in your app or you have a custom hook, and there you keep the whole logic for adding/removing/displaying messages.

If you use application-level error handling, you can pass error messages to your messages/notification manager and do whatever you want with them.

There are two types of errors.

1. GraphQL errors (like in a previous example)

2. Network error (for example, if the app lost internet connection)

### GraphQL errors

There are three types of GraphQL errors:

- **syntax error** - for example, when you made a mistake in a query or mutation

- **resolver error** - for example, when the GraphQL server was not able to resolve a query field

- **validation error** - for example, when provided data didn't pass validation on the server side.

Note that when there is a resolver error, the GraphQL server returns partial data, but if there is a syntax or validation error, the server doesn't return data at all.

In the first case, the server responds with a **200** status code, otherwise returns a **4xx** status code (for syntax and validation errors)

### Network errors

Network errors occur when there are communication problems with the GraphQL server. In this case, the server usually responds with a **4xx** or **5xx** response status code and no data.

### Error policies

By default, the [[Introduction to the Apollo local state and reactive variables|Apollo]] server returns partial data when there is a resolver error, but you can change this behavior by changing the error policy. There are three error policies:

- **none** \- the default one - if there are errors the `graphQLErrorsthe` field is populated and the `data` field is set to undefined (even if the server returns some data in response)

- **all** \- both fields `data` and `graphQLErrors` are populated

- **ignore** \- `graphQLErrors`field is ignored and not populated

#### How to specify error policy

You can specify error policy globally on or query/mutation level.

##### Global error policy

You can set an error policy for [[How to mock GraphQL queries and mutations|queries and mutations]] using the `defaultOptions` object in the ApolloClient constructor. The example below shows an error policy all set for queries and an ignore policy for mutations.

```javascript
import { ApolloClient, InMemoryCache } from "@apollo/client";

const client = new ApolloClient({
  cache: new InMemoryCache(),
  uri: "http://localhost:3000/",
  defaultOptions: {
    query: {
      errorPolicy: "all",
    },
    mutate: {
      errorPolicy: "ignore",
    },
  },
});
```

#### Operation error policy

To specify error policy on the operation level, you have to pass the `errorPolicy` field in options object like this:

```javascript
const { loading, error, data } = useQuery(YOUR_QUERY, {
  errorPolicy: "ignore",
});
```

### Implement application-level error handling

To implement application-level error handling, we need to use a functionality called **ApolloLink**.

The Apollo Link library helps you customize the data flow between Apollo Client and your **GraphQL** server. You can define your client's network behavior as a chain of **link** objects that execute in a **sequence**.

Each link should represent either a self-contained modification to a [[How to create a quick search component using Apollo lazy query|GraphQL]] operation or a side effect (such as logging).

Take a look at a sample implementation of application-level error handling.

First, import the **onError** function.

```javascript
import { onError } from "@apollo/client/link/error";
```

Second, create the **errorLink**:

```javascript
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    console.log(graphQLErrors);
  }

  if (networkError) {
    // handle network error
    console.log(networkError);
  }
});
```

Third, use **HttpLink**, and from helper method to combine a single link that can be used in the Apollo client.

```javascript
import { ApolloClient, InMemoryCache, ApolloProvider, from, HttpLink } from '@apollo/client';

...

const httpLink = new HttpLink({ uri: 'https://<API_URL>' })

const appLink = from([
    errorLink, httpLink
])

const client = new ApolloClient({
    link: appLink,
    cache: new InMemoryCache(),

});
```

---

## Summary

There are two types of errors that you can handle:

1. network errors

2. GraphQL error

There are three error policies (all, ignore, and none), and you can specify an error policy globally or on the operation level.

Moreover, there are two levels where you can handle those errors:

1. application level

2. component (query/mutation) level

Thanks to application-level error handling, you can use JavaScript error tracking tools on production and log errors to the console in local environments. Besides, you can use this mechanism to handle and display errors in your application.

#WebDevelopment #FrontendDevelopment #BackendDevelopment #JavaScript #React #GraphQL #ApolloClient #ConceptExplanation #Tutorial #BestPractices #Intermediate #ErrorHandling #APIIntegration