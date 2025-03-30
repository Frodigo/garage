*Last updated: 16/09/2022*

Nowadays, distributed architectures of software have become more popular, and along with the trend, software teams use the API-first approach to building products.

On the other hand, architects and developers decide to use the GraphQL API instead of REST more and more (but REST APIs are still good for sure)

I will not cite the well-known advantages and disadvantages of GraphQl here, but I want to stand the one that is not well-known but is quite important for developers:

> **One of the most significant advantages of using GraphQL is that a frontend developer can quickly mock sample data, and switch to real data when the backend is done.**

## What exactly is mock-up data?

Suppose some functionality needs data from the backend or somehow needs to communicate with the API, and this data is not available, or the API hasn’t been done yet. In that case, the Front-end developer needs to mock up some sample data. Take a look at the examples below:

### 1\. Displaying additional information about a product

A development team is working on displaying additional information about a product on a product page. The data are called “Key features” and consist of an image, a name, and a description. This data will come from the backend. The backend team hasn’t started working on this functionality yet, so the Frontend developer decides to mock up this data and display this mockup on the front end. When the backend is done, the mockup data will be replaced with real data.

### 2\. Sending a message to a seller

This functionality lets customers send a message to a seller. A customer fills out the form. He enters his name, surname, e-mail address, and message. Additionally, they must accept consent to the processing of personal data. The frontend developer has already built the form and validation and is at the stage of sending the form to the backend. The backend must pick up the form and return a success or error message, and this message will be displayed to the user. The backend part is not ready yet, so the Frontend developer needs to mock this interaction with the backend.

In summary, when some data like fields or even data collections have not been done yet in backend implementation, developers use fake values (mock data) and replace them with real data when the backend is ready.

In this article, I show how to mock:

- single fields

- queries

- mutation

In the end, I will show you how to easily replace mock data with real backend data.

With this knowledge, you will be able to work on your front end more efficiently, even when the back end is lagging far behind.

---

## Prerequisites

Computer with a text editor, NodeJS, internet connection, basic JavaScript, React, and GraphQL skills.

## Create react app

I use [create-react-app](https://create-react-app.dev/docs/getting-started) to scaffold a new project:

```bash
npx create-react-app graphql-mocks
cd graphql-mocks
npm start
```

## Install Apollo Client

Next, I use the command line to install the apollo client:

```bash
npm install @apollo/client graphql
```

Apollo client allows connecting with GraphQL server and performing GraphQL operations like queries and mutations thanks to custom React hooks like useQuery or useMutation.

## Initialize Apollo client

Once the client is installed, I can connect my front end with GraphQL API. This time I am going to use publically available [SpaceX GraphQL API](https://api.spacex.land/graphql/).

First, I import Apolo Client, InMemoryCache, and ApolloProvider from @apollo/client.

```javascript
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
```

Second, I initialize the client:

```javascript
const client = new ApolloClient({
  uri: "https://api.spacex.land/graphql/",
  cache: new InMemoryCache(),
});
```

That is the minimal config needed to make Apollo Client working - URL to API and in-memory cache initialized.

Third, I wrap the App component by ApolloProvider:

```javascript
<ApolloProvider client={client}>
  <App />
</ApolloProvider>
```

ApolloProvided takes one argument: a client that we have already initialized. Once I wrap the App component with ApolloProvider, I can use the client in the App component and every child of the app component.

## How to mockup single fields

In this example, I show you how to fetch existing fields from the API and how to add a field that doesn't exist in the response.

### Create the missions component

In the beginning, I create the Missions component that will be responsible for displaying missions.

Create components \\ missions \\ Missions.jsx file:

```javascript
export const Missions = () => {
  return (
    <>
      <h1>Missions</h1>
      Missions will be listed here
    </>
  );
};
```

Create components \\ missions \\ index.js file:

```javascript
export { Missions } from "./Missions";
```

Create components \\ index.js file:

```javascript
export { Missions } from "./missions";
```

Import Missions component in the App.js:

```javascript
import { Missions } from "./components";
```

Render component:

```javascript
function App() {
  return (
    <main className="container">
      <Missions />
    </main>
  );
}
```

Add styles to App.css:

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
}
```

---

### The query for the data

I want to fetch missions from the graphql server. To do so, I need to define a query.

I add file components \\ missions\\ missions.gql.js:

```javascript
import { gql } from "@apollo/client";

export default gql`
  {
    missions(limit: 10) {
      description
      id
      manufacturers
      name
      twitter
      website
      wikipedia
    }
  }
`;
```

I import the query and useQuery hook in components \\ Missions \\ missions.jsx:

```javascript
import { useQuery } from "@apollo/client";
import MISSIONS_QUERY from "./missions.gql.js";
```

I use the useQuery hookto fetch graphql data:

```javascript
const { loading, error, data } = useQuery(MISSIONS_QUERY);
```

I add a little logic to handle loading and errors state:

```javascript
if (loading) return null;
if (error) return `Error! ${error}`;
if (!data?.missions?.length) {
  return "No missions found";
}

const { missions } = data;
```

Finally, I render data returned from API:

```javascript
{
  missions.map((mission) => {
    return (
      <div className="mission" key={mission.id}>
        <h2>{mission.name}</h2>
        <p>{mission.description}</p>
        <h3>Manufacturers:</h3>
        <ol>
          {mission.manufacturers?.map((manufacturer) => (
            <li key={`${mission.id}-${manufacturer}`}>{manufacturer}</li>
          ))}
        </ol>
        <h3>Links:</h3>
        <ul>
          {mission.twitter?.length && (
            <li>
              <a href={mission.twitter}>{mission.twitter}</a>
            </li>
          )}
          {mission.website?.length && (
            <li>
              <a href={mission.website}>{mission.website}</a>
            </li>
          )}
          {mission.wikipedia?.length && (
            <li>
              <a href={mission.wikipedia}>{mission.wikipedia}</a>
            </li>
          )}
        </ul>
      </div>
    );
  });
}
```

The complete code of the component looks like this:

```javascript
import { useQuery } from "@apollo/client";
import MISSIONS_QUERY from "./missions.gql.js";

export const Missions = () => {
  const { loading, error, data } = useQuery(MISSIONS_QUERY);

  if (loading) return null;
  if (error) return `Error! ${error}`;
  if (!data?.missions?.length) {
    return "No missions found";
  }

  const { missions } = data;

  return (
    <>
      <h1>Missions</h1>
      {missions.map((mission) => {
        return (
          <div className="mission" key={mission.id}>
            <h2>{mission.name}</h2>
            <p>{mission.description}</p>
            <h3>Manufacturers:</h3>
            <ol>
              {mission.manufacturers?.map((manufacturer) => (
                <li key={`${mission.id}-${manufacturer}`}>{manufacturer}</li>
              ))}
            </ol>
            <h3>Links:</h3>
            <ul>
              {mission.twitter?.length && (
                <li>
                  <a href={mission.twitter}>{mission.twitter}</a>
                </li>
              )}
              {mission.website?.length && (
                <li>
                  <a href={mission.website}>{mission.website}</a>
                </li>
              )}
              {mission.wikipedia?.length && (
                <li>
                  <a href={mission.wikipedia}>{mission.wikipedia}</a>
                </li>
              )}
            </ul>
          </div>
        );
      })}
    </>
  );
};
```

### Extend GraphQL schema on the client side

Here, the main topic of the article begins! The Missions component renders some data about missions on the front like description, name, web links and so on.

I want to mock one single field, which is a sponsors field, and it is an array of strings. To do so, I create the graphql-type-defs.js file in the root of the project with the following content:

```javascript
import { gql } from "@apollo/client";

export default gql`
  extend type Mission {
    sponsors: [String]
  }
`;
```

That schema definition extends the Mission type and ads sponsors field to it.

Now I import my type definition in the index.js file:

```javascript
import typeDefs from "./graphql-type-defs";
```

And pass it to the ApolloClient constructor:

```javascript
const client = new ApolloClient({
  uri: "https://api.spacex.land/graphql/",
  cache: new InMemoryCache(),
  typeDefs,
});
```

### Define a read function with mock data

The Next step is to define a custom read function to produce mock data for us.

Before I do that, I install FakerJS. it's a library (fake data generator) that helps produce fake and random data.

```
npm install @faker-js/faker --save-dev
```

Then, I pass the configuration with object types policies to the InMemoryCache constructor:

```javascript
cache: new InMemoryCache({
    typePolicies: {
        Mission: {
            fields: {
                sponsors: {
                    read() {
                        return [...faker.random.words(faker.datatype.number({
                            'min': 1,
                            'max': 5
                        })).split(' ')]
                    }
                },
            },
        },
    },
}),
```

That code defines the read() function for the sponsors' field of the Mission type. The read() function returns fake objects. In this case, it returns a new array of from one to five elements. Elements in that array are random words.

### Query with the @client directive and display data

To fetch the mock field, I need to add it to the query. To make it work, I need to use the @client directive. Take a look at the updated missions query:

```javascript
export default gql`{
  missions(limit: 10) {
    description
    id
    manufacturers
    name
    twitter
    website
    wikipedia
    sponsors @client // here you go
  }
}
`;
```

Finally, I can render the sponsors field on the front end. I add this code to the render function of the missions component:

```javascript
<h3>Sponsors:</h3>
<ol>
    {mission.sponsors?.map(sponsor => <li key={`${mission.id}-${sponsor}`}>{sponsor}</li>)}
</ol>
```

---

## How to mockup an entire query

Mocking single fields is so useful. Moreover, sometimes devs want to mock a query or mutation that doesn't exist in the backend. Let's start by mocking a query.

### Add a new query to the schema

Let's add the publications query that returns an array of publications (name of the publication and URL).

I extend the graphql-type-defs.js by adding new types:

```javascript
type Query {
    publications: [Publication]
}

type Publication {
    name: String!
    url: String!
 }
```

### Define resolver

Next, I need to define a resolver that will produce fake data for the publications query.

I create a graphql-resolvers.js file:

```javascript
import { faker } from "@faker-js/faker";

export default {
  Query: {
    publications: () => {
      const publications = [];
      const publicationLength = faker.datatype.number({
        min: 1,
        max: 5,
      });

      for (let i = 0; i < publicationLength; i++) {
        publications.push({
          name: faker.lorem.sentence(),
          url: faker.internet.url(),
        });
      }
      return publications;
    },
  },
};
```

I defined the publications function that returns a new array of fake publications.

### Register resolver

To register the resolver, you need to pass it to the ApolloClient constructor:

```javascript
import resolvers from "./graphql-resolvers";

const client = new ApolloClient({
  uri: "https://api.spacex.land/graphql/",
  cache: new InMemoryCache({
    typePolicies: {
      Mission: {
        fields: {
          sponsors: {
            read() {
              return [
                ...faker.random
                  .words(
                    faker.datatype.number({
                      min: 1,
                      max: 5,
                    }),
                  )
                  .split(" "),
              ];
            },
          },
        },
      },
    },
  }),
  typeDefs,
  resolvers, // here you go
});
```

### Use mocked query in the app

Let's create the publications component that displays mocked data.

components \\ publications \\ Publications.jsx

```javascript
import { useQuery } from "@apollo/client";
// 1. here is imported the publications query
import PUBLICATIONS_QUERY from "./publications.gql.js";

export const Publications = () => {
  // 2. here the query is used
  const { loading, error, data } = useQuery(PUBLICATIONS_QUERY);

  if (loading) return null;
  if (error) return `Error! ${error}`;
  if (!data?.publications?.length) {
    return "No publications found";
  }

  const { publications } = data;

  return (
    <>
      <h1>Publications</h1>
      <ol>
        {publications?.map((publication) => (
          <li key={publication.name}>
            <a href={publication.url}>{publication.name}</a>
          </li>
        ))}
      </ol>
    </>
  );
};
```

(1.) I imported the publications query in this place, and here (2.) I used in it the useQuery hook.

As you can see from the component and useQuery hook perspective, it's not important if the quarry that is used is fake or real. It's transparent and works in the same way.

components \\ publications \\ publications.gql.js:

```javascript
import { gql } from "@apollo/client";

export default gql`
  {
    publications @client {
      name
      url
    }
  }
`;
```

Directive @client allows defining not only fields like in the previous example but also queries and mutations.

components \\ publications \\ index.js:

```javascript
export { Publications } from "./Publications";
```

components \\ index.js:

```javascript
export { Publications } from "./publications"; // added this import
export { Missions } from "./missions";
```

Add the publication component in the App.js:

```javascript
import './App.css';
import {Missions, Publications} from "./components"; // added import

function App() {
  return <main className="container">
    <Missions/>
    <Publications/> !<-- added component -->
  </main>
}

export default App;
```

---

## Ho to mock a graphql mutation

The last example I want to show is how to mock a graphql mutation. Let's implement a simple form that allows users to submit a new publication. The form has two inputs: the title of the publication and its URL.

---

## Add the PublicationForm component

Create a file components \\ PublicationForm \\ PublicationForm.jsx

```javascript
import { useCallback, useState } from "react";

export const PublicationForm = () => {
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");

  const submitForm = useCallback(
    (e) => {
      e.preventDefault();
      console.log(title, url);
    },
    [title, url],
  );
  return (
    <form onSubmit={submitForm}>
      <legend>Submit a new publication:</legend>
      <input
        type="text"
        placeholder="Publication title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Publication URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
};
```

So there are two fields in the form and the submit button. When a user clicks submit, the submitForm function is called. For now, it only logs to the console.

Create a file components \\ publicationForm \\ index.js

```javascript
export { PublicationForm } from "./PublicationForm";
```

Re-export component in components/index.js:

```javascript
export { Publications } from "./publications";
export { Missions } from "./missions";
export { PublicationForm } from "./publicationForm"; // added here
```

Add the component to the render function of the app component:

```javascript
import "./App.css";
import { Missions, Publications, PublicationForm } from "./components";

function App() {
  return (
    <main className="container">
      <Missions />
      <Publications />
      <PublicationForm />
    </main>
  );
}

export default App;
```

## Add the mutation to the schema

Let's define a new mutation in our graphql schema:

```javascript
type Mutation {
  addPublication(name: String!, url: String!): String
}
```

The final graphql-type-defs looks like this:

```javascript
import { gql } from "@apollo/client";

export default gql`
  extend type Mission {
    sponsors: [String]
  }

  type Query {
    publications: [Publication]
  }

  type Mutation {
    addPublication(name: String!, url: String!): String
  }

  type Publication {
    name: String!
    url: String!
  }
`;
```

## Define a resolver for the mutation

Now, I am gonna add the addPublication mutation resolver to the graphql-resolvers.js file:

```javascript
import { faker } from "@faker-js/faker";

export default {
  Query: {
    // query resolvers
  },

  Mutation: {
    addPublication: (parent, args, context, info) => {
      console.log(parent, args, context, info);
      return "Your publication has been submitted, thank you!";
    },
  },
};
```

I defined the mutation, and it returns a string. Of course, if you need more sophisticated testing of mocked mutation, you can add code here.

## How to use mocked mutation in the app

Add components \\ publicationForm \\ addPublication.gql.js file:

```javascript
import { gql } from "@apollo/client";

export default gql`
  mutation addPublication($name: String!, $url: String!) {
    addPublication(name: $name, url: $url) @client
  }
`;
```

As you can see, here also I used the @client directive to define mock mutation

Update the publicationForm.jsx component code:

```javascript
import { useCallback, useMemo, useState } from "react";
import { useMutation } from "@apollo/client";
import ADD_PUBLICATION_MUTATION from "./addPublication.gql";

export const PublicationForm = () => {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [addPublication, { data, loading, error }] = useMutation(
    ADD_PUBLICATION_MUTATION,
  );

  const submitForm = useCallback(
    (e) => {
      e.preventDefault();
      addPublication({ variables: { name, url } });
    },
    [name, url, addPublication],
  );

  const results = useMemo(() => {
    return data?.addPublication;
  }, [data]);

  if (loading) return null;
  if (error) return `Error! ${error}`;

  return (
    <form onSubmit={submitForm}>
      <legend>Submit a new publication:</legend>
      <input
        type="text"
        placeholder="Publication title"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Publication URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button type="submit">Submit</button>
      <div>{results}</div>
    </form>
  );
};
```

Here I added the logic responsible for performing mutation. As for queries - it work the same with mocked mutation as with real ones.

---

## How to use live data when it is ready

Ok, so we have mocked some fields, queries, and mutations, and you may ask what you should do when the backend team implements all requested fields and operations in the API.

It's pretty simple. You should:

1. 1\. remove @client annotations - when a particular field or operation is ready, just remove the @client directive from query/mutation

2. 2\. remove client resolvers - remove resolvers because they are not needed anymore when data is populated from API

3. 3\. remove client type definitions - same here, the schema should be implemented on the backend side, so it's no need anymore

---

## Summary

In this article, I showed you how to mock GraphQL queries and mutations. Compared to a REST API, mocking GraphQL queries is much easier. The subsequent transition to real data only really involves a change in [[The full-stack guide to the GraphQL query|GraphQL queries]] and resolvers’ removal. In my opinion, mocking data in GraphQL is much easier than in REST, which is unquestionably beneficial for everyone.

When you want to mock some fields or operations on the client side using Apollo Client, please follow these steps:

1. Create client-side GraphQL schema

2. Define custom resolvers/read function

3. Use @client directive in queries/mutations

I hope you liked this article. Thanks for reading!
