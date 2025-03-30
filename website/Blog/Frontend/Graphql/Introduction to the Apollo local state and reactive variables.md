*Last updated: 13/10/2022*

In one of my previous articles, I described the useReducer hook as an excellent way to manage the state of React apps, including apps connected with GraphQL APIs using the apollo client.

Typically in an app, you have a remote state (from sever, for API, here I mean from GraphQL API), but also you can have a local state that does not exist on the server side.

I said that useReducer is suitable for managing situations like that – moreover – using Apollo Client, there is another way to manage the local state.

## Apollo Client for State Management

Apollo client 3 enables the management of a local state by incorporating field policies and reactive variables. Field Policy lets you specify what happens if you query specific fields, including those not specified for your GraphQL servers. Field policies define local fields so the field is populated with information stored anywhere, like local storage and reactive variables.

So Apollo Client (version >=3) provides two mechanisms to handle the local state:

- Local-only fields and field policies

- Reactive variables

### What is the Apollo client?

The Apollo client connects React App and GraphQL API. Moreover, it is a state management library.

It helps you to connect your React App with GraphQL API. It provides methods to communicate with API, cache mechanisms, helpers, etc.

Besides, Apollo client provides an integrated state management system that allows you to manage the state of your whole application.

---

### What is Apollo State?

Apollo Client has its state management system using GraphQL to communicate directly with external servers and provide scalability.

Apollo Client supports managing the local and remote state of applications, and you will be able to interact with any state on any device with the same API.

## Local-only fields and field policies

This mechanism allows you to create your client schema. You can extend a server schema or add new fields.

Then, you can define field policies that describe wherefrom data came from. You can use Apollo cache or local storage.

The crucial advantage of this mechanism is using the same API as when you work with server schema.

### Local state example

If you want to handle local data inside a standard GraphQL query, you have to use a @client directive for local fields:

```javascript
query getMissions ($limit: Int!){
    missions(limit: $limit) {
        id
        name
        twitter
        website
        wikipedia
        links @client // this field is local
    }
}
```

### Define local state using local-only fields

#### InMemory cache from Apollo

Apollo client provides a caching system for local data. Normalized data is saved in memory, and thanks to that, already cached data can get fast.

#### Field type policies

You can read and write to the Apollo client cache. Moreover, you can customize how a specific field in your cache is handled. You can specify read, write, and merge functions and add custom logic.

To define a local state, you need to:

1. Define field policy and pass it to the InMemoryCache

2. Add field to the query with @client directive

### Local-only fields tutorial

Let's go deeper with the local-only field and check how they work in action.

#### Initialize the project using Create React App

```bash
npx create-react-app local-only-fields
```

#### Install apollo client

```bash
npm install @apollo/client graphql   
```

#### Initialize Apollo client

Import apollo client stuff in index.js:

```javascript
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
```

Create client instance

```javascript
const client = new ApolloClient({
  uri: "https://api.spacex.land/graphql/",
  cache: new InMemoryCache(),
});
```

API.spacex.land/graphql is a fantastic free public demo of GraphQL API, so I use it here. If you want to explore that API, copy the URL to the browser: [https://api.spacex.land/graphql/](https://api.spacex.land/graphql/)

Connect Apollo with React by wrapping the App component with ApolloProvider:

```javascript
<ApolloProvider client={client}>
       
  <App />
</ApolloProvider>
```

ApolloProvider takes the client argument, which is our already declared Apollo Client. We can use Apollo Client features in the App component and every child component, thanks to that.

#### The query for missions data

Let's get some data from the API. I want to get missions:

```javascript
query getMissions ($limit: Int!){
  missions(limit: $limit) {
    id
    name
    twitter
    website
    wikipedia
  }
}
```

Results for this query when I passed 3 as a limit variable:

```json
{
  "data": {
    "missions": [
      {
        "id": "9D1B7E0",
        "name": "Thaicom",
        "twitter": "https://twitter.com/thaicomplc",
        "website": "http://www.thaicom.net/en/satellites/overview",
        "wikipedia": "https://en.wikipedia.org/wiki/Thaicom"
      },
      {
        "id": "F4F83DE",
        "name": "Telstar",
        "twitter": null,
        "website": "https://www.telesat.com/",
        "wikipedia": "https://en.wikipedia.org/wiki/Telesat"
      },
      {
        "id": "F3364BF",
        "name": "Iridium NEXT",
        "twitter": "https://twitter.com/IridiumBoss?lang=en",
        "website": "https://www.iridiumnext.com/",
        "wikipedia": "https://en.wikipedia.org/wiki/Iridium_satellite_constellation"
      }
    ]
  }
}
```

Let's create a React component that receives that data and, for now, displays the name of the Mission on the screen.

First, create a unit test: src/components/Missions/\_\_tests\_\_/Missions.spec.js

```javascript
import { render } from "@testing-library/react";
import Missions from "../Missions";
describe("Missions component", () => {
  it("Should display name of each mission", () => {
    const { getByText } = render(<Missions />);
    getByText("Missions component should be here.");
  });
});
```

Of course, the test fails because we event doesn't have a component created yet.

Add Component: src/components/Missions/Missions.js

```javascript
import React from "react";
export const Missions = () => {
  return <div>       Missions component should be here.    </div>;
};
export default Missions;
```

Now the test is passing


Let's re-export component in src/components/Missions/index.js

```javascript
export { default } from "./Missions";
```

We need to query for data using the useQuery hook provided by the Apollo client.

In unit tests, you need to have a component wrapped by **ApolloProvider**. For testing purposes, Apollo provides a unique Provider: **MockedProvider,** and it allows you to add some mock data. Let's use it.

```javascript
// src/components/Missions/__tests__/Missions.spec.js

import MockedProvider:
 
import { MockedProvider } from '@apollo/client/testing';
```

Define mocks:

```
const mocks = [
   {
       request: {
           query: GET_MISSIONS,
           variables: {
               limit: 3,
           },
       },
       result: {
           "data": {
               "missions": [
               {
                   "id": "9D1B7E0",
                   "name": "Thaicom",
                   "twitter": "https://twitter.com/thaicomplc",
                   "website": "http://www.thaicom.net/en/satellites/overview",
                   "wikipedia": "https://en.wikipedia.org/wiki/Thaicom"
               },
               {
                   "id": "F4F83DE",
                   "name": "Telstar",
                   "twitter": null,
                   "website": "https://www.telesat.com/",
                   "wikipedia": "https://en.wikipedia.org/wiki/Telesat"
               },
               {
                   "id": "F3364BF",
                   "name": "Iridium NEXT",
                   "twitter": "https://twitter.com/IridiumBoss?lang=en",
                   "website": "https://www.iridiumnext.com/",
                   "wikipedia": "https://en.wikipedia.org/wiki/Iridium_satellite_constellation"
               }
               ]
           }
       }
   },
];
```

The test fails because we don't have the GET_MISSIONS query defined yet.


Create the file queries/missions.gql.js with the following content:

```javascript
import { gql } from "@apollo/client";
export const GET_MISSIONS = gql`
   query getMissions ($limit: Int!){
       missions(limit: $limit) {
           id
           name
           twitter
           website
           wikipedia
       }
   } 
`;
```

Import query in the src/components/Missions/\_\_tests\_\_/Missions.spec.js

```javascript
import { GET_MISSIONS } from "../../../queries/missions.gql";
```

Now let's wrap the Missions component by the Mocked provider.

```javascript
const { getByText } = render(
  <MockedProvider mocks={mocks}>
          
    <Missions />
       
  </MockedProvider>,
);
```

Now, we can expect that three product missions are visible on the screen because, in our mock response, we have an array with three missions with corresponding names: 'Thaicom,' 'Telstar,' and 'Iridium NEXT.'

To do so, update the test case.

First, make the test case asynchronous by adding the async keyword before **the it** callback function.

Second, replace the **getByText** query with the **findByText,** which works asynchronously.

```javascript
it("Should display name of each mission", async () => {
  const { findByText } = render(
    <MockedProvider mocks={mocks}>
                     
      <Missions />
                 
    </MockedProvider>,
  );
  await findByText("Thaicom");
  await findByText("Telstar");
  await findByText("Iridium NEXT");
});
```

The test fails because we don't query for the data in React component.

By the way, maybe, you think I don't wrap findBytext by the **expect…toBe**. I do not do that because the findByText query throws an error when it cannot find provided text as an argument, so I don't have to create an assertion because the test will fail if the text is not found.

Let's update the React component.

First import useQuery hook, and GET_MISSIONS query in src/components/Missions/Missions.js

```javascript
import { useQuery } from "@apollo/client";
import { GET_MISSIONS } from "../../queries/missions.gql";
```

Let's query for the data in the component body:

```javascript
const { data } = useQuery(GET_MISSIONS, {
  variables: {
    limit: 3,
  },
});
```

Now, let's prepare content that Component will render for us. If missions exist, allow's display the name of each Mission. Otherwise, let's show the 'There is no missions' paragraph.

```javascript
const shouldDisplayMissions = useMemo(() => {
  if (data?.missions?.length) {
    return data.missions.map((mission) => {
      return (
        <div key={mission.id}>
          <h2>{mission.name}</h2>
        </div>
      );
    });
  }

  return <h2>There are no missions</h2>;
}, [data]);
```

In the end, the Component needs to return shouldDisplayMissions:

```javascript
import React, { useMemo } from "react";
import { useQuery } from "@apollo/client";
import { GET_MISSIONS } from "../../queries/missions.gql";
export const Missions = () => {
  const { data } = useQuery(GET_MISSIONS, {
    variables: {
      limit: 3,
    },
  });
  const shouldDisplayMissions = useMemo(() => {
    if (data?.missions?.length) {
      return data.missions.map((mission) => {
        return (
          <div key={mission.id}>
                               <h2>{mission.name}</h2>
                           
          </div>
        );
      });
    }
    return <h2>There are no missions</h2>;
  }, [data]);
  return shouldDisplayMissions;
};
export default Missions;
```

Now, the test pass!

The last thing for this step is to inject components into the app and see missions in the browser.

```javascript
// App.js

import Missions from "./components/Missions";
function App() {
  return <Missions />;
}
export default App;
```

It works but, initially, it shows, "There are no missions." Let fix it by adding a loading indicator in Missions.js.

First, grab the loading flag from the useQuery hook results:

```javascript
const { data, loading } = useQuery(GET_MISSIONS, {
  variables: {
    limit: 3,
  },
});
```

Add loading indicator:

```
if (loading) {
    return <p>Loading...</p>
}

return shouldDisplayMissions;
```

Besides, add a little bit of styling.

```javascript
//src/components/Missions/Missions.module.css
.mission {
   border-bottom: 1px solid black;
   padding: 15px;
}
```

Now, import CSS module in Missions.js file:

```
import classes from './Missions.module.css'
```

and add mission class to the mission div:

```javascript
return (
  <div key={mission.id} className={classes.mission}>
    <h2>{mission.name}</h2>
  </div>
);
```


---

## Add local-only field

OK, so we have data from API. The next task is to display links for the Mission. API returns three fields:

- twitter

- website

- Wikipedia

We can create our local field called: **links**. It will be an array with links, so we can loop through that array and just display links.

First, let's add a new test case:

```javascript
it("Should display links for the mission", async () => {
  const localMocks = [
    {
      ...mocks[0],
      result: {
        data: {
          missions: [
            {
              id: "F4F83DE",
              name: "Telstar",
              links: ["https://www.telesat.com/"],
            },
          ],
        },
      },
    },
  ];
  const { findByText } = render(
    <MockedProvider mocks={localMocks}>
      <Missions />
    </MockedProvider>,
  );

  await findByText('https://www.telesat.com/"');
});
```

So, we expect that there will be rendered one link: "[https://www.telesat.com/](https://www.telesat.com/)"

### Define field policy

First, we must define the field policy for our local links field.

When you inspect docs for missions query in GraphQL API, you can see that it returns a Mission type.

So we need to add a links client field to the Mission type.

To do so, we need to add a configuration to InMeMoryCache in the src/index.js file like this:

```javascript
const client = new ApolloClient({
 uri: 'https://api.spacex.land/graphql/',
 cache: new InMemoryCache({
   typePolicies: {
     Mission: {
       fields: {
         links: {
           read(_, { readField }) {
             // logic will be added here in the next step
           }
         }
       }
     }
   }
 })
```

Now let's return an array with links collected from the Mission. The read function has two arguments. The first one is the field's currently cached value if one exists. The second one is an object that provides several properties and helper functions. We will use the readField function to read other field data.

Our logic for the links local field:

```javascript
read(_, { readField }) {
    const twitter = readField('twiiter');
    const wikipedia = readField('wikipedia');
    const website = readField('website');
    const links = [];


    if (twitter) {
      links.push(twitter);
    }


    if (wikipedia) {
      links.push(wikipedia);
    }


    if (website) {
      links.push(website);
    }


    return links;
  }
```

### The query for local-only field

The next step is to include the links field in the query. Let's modify the GET_MISSIONS query:

```javascript
query getMissions ($limit: Int!){
    missions(limit: $limit) {
        id
        name
        twitter
        website
        wikipedia
        links @client
    }
}
```

You can define the local-only field by adding the @client directive after the field name.

### Display local-only field on the screen

We have made good progress, but the test still fails because the Component does not render any links yet.

Please update the Missions component by modifying the shouldDisplayMissions Memo function.

```javascript
const shouldDisplayMissions = useMemo(() => {
  if (data?.missions?.length) {
    return data.missions.map((mission) => {
      const shouldDisplayLinks = mission.links?.length
        ? mission.links.map((link) => {
            return (
              <li key={`${mission.id}-${link}`}>
                <a href={link}>{link}</a>
              </li>
            );
          })
        : null;

      return (
        <div key={mission.id} className={classes.mission}>
          <h2>{mission.name}</h2>
          {shouldDisplayLinks}
        </div>
      );
    });
  }

  return <h2>There are no missions</h2>;
}, [data]);
```

We are good now. Everything work as well in the browser:

---

## Working Demo

Here you can see the demo of the app:

[https://apollo-client-local-only-fields-tutorial.vercel.app/](https://apollo-client-local-only-fields-tutorial.vercel.app/)

## **Source code**

Here you can find the source code for this tutorial: [https://github.com/Frodigo/apollo-client-local-only-fields-tutorial](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial)

Here are the commits for each step:

1. [Initialize the project using Create React App](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial/commit/57cef8a41077571f8a60675ec81882d8b71a6b89)

2. [Install Apollo Client](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial/commit/595bf812f93c9a104d1f6983c6d046d432104bbe)

3. [Initialize Apollo Client](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial/commit/e32ab19d6a54b70bb44d92a2754a9538c73ad667)

4. [The query for missions data](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial/commit/0212eeca03b4768c1b163da355083e984e276668)

5. [Add local-only field](https://github.com/Frodigo/apollo-client-local-only-fields-tutorial/commit/71b004f013826c4eb58da045230d36334716acde)

## Reactive variables

OK, you met local-only fields, and now let's look at another mechanism called: Reactive variables.

You can write and read data anywhere in your app using reactive variables.

Apollo client doesn't store reactive variables in its cache, so you don't have to keep the strict cached data structure.

Apollo client detects changes in reactive variables, and when the value changes, a variable is automatically updated in all places.

### Reactive variables in action

This time I would like to show you the case using reactive variables. I don't want to repeat Apollo docs, so you can see the basics of reading and modifying reactive variables [here](https://www.apollographql.com/docs/react/local-state/reactive-variables/).

### The case

I've started work on the cart and mini-cart in my react-apollo-storefront app. The first thing that I needed to do was create an empty cart.

In Magento GraphQL API, there is the mutation **createEmptyCart**. That mutation returns the cart ID.

I wanted to get a cart ID, store it in my app, and after the page refresh, check if a value exists in the local state and, if yes, get it from it without running mutation.

### Implementation

First, let's define the reactive variable:

```javascript
import { makeVar } from "@apollo/client";

export const CART_ID_IDENTIFER = "currentCardId";
export const cartId = makeVar(localStorage.getItem(CART_ID_IDENTIFER));
```

Second, use that variable in a component, context, or hook and make it reactive:

```
import { useReactiveVar } from '@apollo/client';

export const CartProvider = ({ children }) => {
    const currentCartId = useReactiveVar(cartId);
};
```

Third, define the mutation to collect a cart Id from the server:

```javascript
// mutation:
import { gql } from "@apollo/client";

export const CREATE_EMPTY_CART = gql`
    mutation createEmptyCart {
        createEmptyCart
    }
`;

// component
// imports
import { useMutation } from "@apollo/client";
import { CREATE_EMPTY_CART } from "../../mutations/cart.gql";

// ... in component body
const [createEmptyCart] = useMutation(CREATE_EMPTY_CART, {
  update(_, { data: { createEmptyCart } }) {
    cartId(createEmptyCart);
    localStorage.setItem(CART_ID_IDENTIFER, createEmptyCart);
  },
});
```

I used the **update** callback there, and I updated the reactive variable:

```
cartId(createEmptyCart)
```

Then I also updated a value in the local storage.

Last, check if the cart ID exists in the local state and if not, send the mutation to a sever.

```javascript
const currentCartId = useReactiveVar(cartId);

useEffect(() => {
  if (!currentCartId) {
    createEmptyCart();
  }
}, [createEmptyCart, currentCartId]);
```

---

## Summary

Today I showed you two techniques for managing local data in Apollo. Local-only fields and reactive variables. Those mechanisms provide a lot of flexibility, and they should be considered when architecting state management in your React application. In addition, I recommend reading about [[How to mock GraphQL queries and mutations|[mocking GraphQL queries and mutation.]]
