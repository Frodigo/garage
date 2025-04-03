---
date: 2022-09-08
title: The full-stack guide to the GraphQL query
---
*Last updated: 08/09/2022*

GraphQL helps prevent the overloading of data. Unlike Restful API, GraphQL allows specifying fields that will be received from the server. That will result in faster communication and less traffic on the network, which will reduce response time considerably. There are two basic types of operations in GraphQL: **queries** and **mutations**.

For reading data, you use query, while for modifying data, you use mutation. The operation is a simple string that allows the server to parse and respond to the data in both cases.

## What is a graphQL query?

Each GraphQL API has a GraphQL schema. The schema describes how data looks and which operations are allowed. So if you have a cars object in your schema, you would query for it. The graphQL query would look like this:

```javascript
query getCars {
  cars {
    brand,
    color
  }
}
```

In the above example, you can see a single graphQL query named **getCars**. In that GraphQL operation, there is the query defined that fetches two fields of **cars** type: *brand* and *color*. I will show you more details about GraphQL queries in this article, but first, let's see how it's possible to execute queries and consume any GraphQL API.

## Prerequisites

In this article, I would like to show you two common things: using a GraphQL query on the client side and writing a basic query using NodeJS.

### GraphQL API

For the first case, you don't need your GraphQL API. You can use some public GraphQL APIs to experiment.

A well-built API to start practicing with is the SpaceX API: [https://api.spacex.land/graphql/](https://api.spacex.land/graphql/)

### Graphql server

In case when you want to create your GraphQL API(with queries), you need to create a GraphQL server. I am going to show you a straightforward example built using **Node** and **ExpressJS**.

## Where do you run a query in GraphQL?

Let's start by consuming SpaceX API to learn fundamentals about graphQL queries. You have at least four options to play with that API:

- using GraphQL Playground

- using GraphiQL Explorer

- using Apollo Studio

- using Chrome extensions like Altair GraphQL

### GraphQL Playground & GraphiQL Explorer

Those are tools that allow you to play with every graphQL API. For example, when you put this URL in the browser: [https://api.spacex.land/graphql/,](https://api.spacex.land/graphql/) you will see GraphiQL explorer. There you can inspect schema, read the docs, run queries, mutations, and so on. GraphQL playground has pretty much the same set of features.

You can set up a playground on the project level or install it for macOS App.

**Note**: GraphQL Playground and GraphiQL are joining forces. More info here: [https://github.com/graphql/graphql-playground/issues/1143](https://github.com/graphql/graphql-playground/issues/1143)

### Apollo Studio

In case when you are creating your graphQL server using [apollo-server](https://github.com/apollographql/apollo-server), you will be able to use Apollo Studio to inspect your API.

### Altair GraphQL Client

Altair client is a Chrome extension that allows you to inspect GraphQL spec, query for all the data, send mutations, use subscriptions, etc.

Today I will use GraphiQL API because the SpaceX API provides it. Typically, you will use tools that are provided with the project/graphQL servers. If you develop your project, you are comfortable to choose own Playground, but this does not matter because soon, both tools will be merged.

Chrome extension is a good choice if you want to check sometimes fast and don't have a chance to use any Playground, but in general, you can use that extension and don't use playgrounds. All of those technics are good enough.

---

## The query for the data

Theory, theory, theory.... let's stop with that and get our hands dirty!

Let's try to get to all users!

```json
{
  users {
    name
    rocket
  }
}
```

### How simple is that?

In the above example, you can see a simple query. The **'users'** objects can be used to request data about all available users – 'users' is an **object** in GraphQL terms. **Objects** hold data about an **entity**. Each object has fields. We used the name and rocket field in our case, but there are more fields for the users' objects. Take a look at the docs:

```json
id: uuid!
name: String
rocket: String
timestamp: timestampt!
twitter: String
```

Some fields cannot be empty (null), and an exclamation mark determines it at the end. That means that, for example, the id cannot be null or undefined. If will be, GraphQL will throw an error.

The results of the following query may look like this:

```json
{
  "data": {
    "users": [
      {
        "name": "sherlock holmes",
        "rocket": "221B Baker Street"
      },
      {
        "name": "sherlock holmes",
        "rocket": "221B Baker Street"
      },
      {
        "name": "sherlock holmes",
        "rocket": "221B Baker Street"
      },
      {
        "name": "sherlock holmes",
        "rocket": "221B Baker Street"
      },
      {
        "name": "User_14211338",
        "rocket": "Space_101010101"
      },
      {
        "name": "Elanthamil",
        "rocket": "Elanthamil"
      }
    ]
  }
}
```

Congratulations! You made your first graphQL query! You are well on your way to becoming a GraphQL master, really!

---

## Query with variables

In the previous example, you have seen a straightforward query (anonymous operation). Now we are going to do something more complicated, like a query with variables. When you want to pass a variable to a graphQL query, you can pass them as parameters:

```javascript
{
  users(limit: 10, order_by: {name: asc}) {
    name
    rocket
  }
}
```

That works in Playground, but it's not too valuable because the values of variables are hardcoded. Let's define a named query using (surprising) a **query** keyword:

```javascript
query getUsers($limit: Int, $orderBy: [users_order_by!]) {
  users(limit: $limit, order_by: $orderBy) {
    name
    rocket
  }
}
```

As you can see here, we have passed two variables: **$limit,** which is a type of Int, and $orderBy, which is a type of \[users_order_by!\].

Types can be primitive like **String**, **Int**, **Float**, **Boolean**, and **ID**, and also you can declare custom types in the [graphQL](https://marcin-kwiatkowski.com/blog/graphql/introduction-to-the-apollo-local-state-and-reactive-variables) schema.

An exclamation mark means that this parameter cannot be empty. You have a special place called "Query variables" (at the bottom). It will help if you put a query variable there. Otherwise, the query will throw an error.

You can also specify a default variable in GraphQL. It works only for non-required arguments. Take a look:

```javascript
query getUsers($limit: Int = 5, $orderBy: [users_order_by!]) {
  users(limit: $limit, order_by: $orderBy) {
    name
    rocket
  }
}
```

## Nested objects

You can request nested fields in a query (based on graphQL schema):

```javascript
query getLaunchesPast($limit: Int = 2) {
  launchesPast(limit: $limit) {
    mission_name
    launch_date_local
    launch_site {
      site_name_long
    }
    rocket {
      rocket_name
      first_stage {
        cores {
          flight
          core {
            reuse_count
            status
          }
        }
      }
    }
  }
}
```

The results may look like this:

```json
{
  "data": {
    "launchesPast": [
      {
        "mission_name": "Starlink-15 (v1.0)",
        "launch_date_local": "2020-10-24T11:31:00-04:00",
        "launch_site": {
          "site_name_long": "Cape Canaveral Air Force Station Space Launch Complex 40"
        },
        "rocket": {
          "rocket_name": "Falcon 9",
          "first_stage": {
            "cores": [
              {
                "flight": 7,
                "core": {
                  "reuse_count": 6,
                  "status": "unknown"
                }
              }
            ]
          }
        }
      },
      {
        "mission_name": "Sentinel-6 Michael Freilich",
        "launch_date_local": "2020-11-21T09:17:00-08:00",
        "launch_site": {
          "site_name_long": "Vandenberg Air Force Base Space Launch Complex 4E"
        },
        "rocket": {
          "rocket_name": "Falcon 9",
          "first_stage": {
            "cores": [
              {
                "flight": 1,
                "core": {
                  "reuse_count": 0,
                  "status": null
                }
              }
            ]
          }
        }
      }
    ]
  }
}
```

## Directives

Directives let you perform a conditional query for objects. There are two types of directives: include and skip. You can pass a bool variable to the query and then use this variable in the directive. Take a look at how it works:

```javascript
query getLaunchesPast($limit: Int = 2, $withRockets: Boolean = false) {
  launchesPast(limit: $limit) {
    mission_name
    launch_date_local
    launch_site {
      site_name_long
    }
    rocket @include(if: $withRockets) {
      rocket_name
      first_stage {
        cores {
          flight
          core {
            reuse_count
            status
          }
        }
      }
    }
  }
}
```

**Note**: Unfortunately, SpaceX API uses an older version of GraphQL tools, and those directives are not supported there.

**Note 2:** GraphQL Server implementations may also add experimental features by defining completely new directives.

## How do GraphQL queries work?

When you want to send a query from the front end, a single request comes to the graphQL server. GraphQL takes a query and looks at what you need, and then a resolver function gets all related data and returns a JSON object.

Theoretically, you can send a request as a simple HTTP request, but a good practice is to use one of the GraphQL clients to communicate with a server. Honestly, in real projects, you have to use the GraphQL client on the front end because it brings a lot of advantages like caching, mechanisms for sending queries, mutations, and so on.

---

## How do I create a query in GraphQL?

I showed you how to send a query. Now let's create our GraphQL server and define a query.

We are going to use NodeJS and Apollo Server to scaffold an app.

The app is a big word. It will be basic stuff. Let's create a query that returns Hello World. It is a fantastic idea, isn't it?

### Set-up a project

Let's init a new project by **npm init command.** Then please install all necessary dependencies**:**

```bash
npm install apollo-server graphql --save
```

### Create an index.js file

Create an index.js file in the src directory(create the directory as well).

Put these imports at the beginning of the file:

```javascript
const { ApolloServer, gql } = require("apollo-server");
```

### Create schema

Let's create theschema. We have to make two types:

1. The Query type with welcomeMessage query

2. The Message type is an object that represents our Message. It has only one field: text which cannot be empty.

Put this code to the file:

```javascript
const typeDefs = gql`
  type Query {
    welcomeMessage: Message!
  }

  type Message {
    text: String!
  }
`;
10;
```

### Create resolver

It's time to create a resolver function for the welcomeMessage query. In real projects, resolvers communicate with databases or other data and collect data. In our trivial example, we want to return a hardcoded string.

Here you go:

```javascript
const resolvers = {
  Query: {
    welcomeMessage: () => {
      return {
        text: "Hello World",
      };
    },
  },
};
```

### Initialize server

The last thing is to create a server instance:

```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

You can run that server by typing *node ./src/index.js* in the console.

Now you can see something like this:

---

## Summary

I hope you enjoyed our quick tour through GraphQL queries. Let me summarize:

- GraphQL has two basic types of operations: queries and mutations

- queries read data. Mutations write data

- there are a few ways to consume or inspecting GraphQL API, like playgrounds and Browser extensions

- graphQL query can be anonymous or can have a name

- you can pass variables to a query

- query variable can have a default value

- each returned field can have a nested object with other data

- There are predefined directives like @include and @skip, and also you can write your directives on the server side.

- To create your graphQL server, you can use Node and Apollo servers.

- Of course, you can even use PHP to write an apollo server, but who wants to write code in PHP?

That essential information should help you to understand the basics of graphQL queries.

#WebDevelopment #BackendDevelopment #API #JavaScript #NodeJS #GraphQL #Apollo #REST #ExpressJS #ConceptExplanation #Tutorial #DeepDive #Intermediate