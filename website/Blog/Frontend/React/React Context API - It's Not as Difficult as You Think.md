*Last update at 03/02/2022*

## A Guide to React Context and useContext() hook

React Context gives data about the components regardless of the level of the component tree. The Context allows managing global data, such as global theme services, user preference, notifications, or more.

On the other hand, you can have Contexts for each more significant part of your app. In case you create an eCommerce react app, you can have Context for cart, the Context for account pages, checkout, and so on.

Context provides data and methods for child components, so the cart needs data about products in the cart. It offers methods to manipulate a cart like adding items, removing, applying discount codes, etc.

I like React because we can find many different solutions for different issues. We have a couple of varying form libraries, lots of CSS libraries, and we have several libraries specifically geared towards state data problems in React. It can be learned by experience in using the library in your project. Sometimes we may install and use libraries that we do not need.

The same is with the state management library. You can use external ones, or you can use context API. It's up to you! It would help if you thought three times before installing any state management library because Context solves issues well in typical cases.

---

## Why Context API?

React enables us to assemble reusable applications with components to repurpose the applications we create. So the React application contains several elements. When an application is rolled out, these components are often significant and unmaintained, which is why we divide them into small parts. This is a fascinating concept in React — you can have lots of components and have an efficient and concise application without having a significant component. When breaking down smaller components for maintenance purposes, they might need a little more data to work correctly.

## Use of provider pattern in React

You probably know about the prop drill. As part of developing an application, you will probably find yourself attempting to drill down layers of components. We have to send props across different levels of components to make them available.

To summarize, prop drilling is a situation when you have to pass down props to a child component, and then to another child, and another.

### Context provides a way to avoid props drilling

Take a look at the example:

```javascript
import React, { useState } from "react";

export const Account = () => {
  const [user, setUser] = useState({ name: "Marcin", country: "Poland" });

  <AccountDetails user={user} setUser={setUser} />;
};

export const EditAccount = (props) => {
  const { user, setUser } = props;

  return (
    <form>
      <input
        type="text"
        value={user.name}
        onChange={(e) =>
          setUser({
            ...user,
            name: e.target.value,
          })
        }
      />

      <input
        type="text"
        value={user.country}
        onChange={(e) =>
          setUser({
            ...user,
            country: e.target.value,
          })
        }
      />
    </form>
  );
};

export const AccountDetails = (props) => {
  const { user, setUser } = props;

  return (
    <>
      <h1>{user.name}</h1>
      <p>Country: {user.country}</p>

      <EditAccount user={user} setUser={setUser}></EditAccount>
    </>
  );
};
```

The Account component passes props user and SetUser to the account details component, and AccountDetailsComponent passes them to the EditAccount component.

Prop drilling, also called threading, is a good and helpful pattern, besides in some cases, you want to avoid using it. Let's consider when you have a notification system in your app. There are two available methods:

1. addMessage

2. removeMessage

You want to have the opportunity to use those methods in any component that you want.

### Parent component -> consuming components communication

To fix the problems with prop drilling, the global object must be accessible in the react tree directly by the components in the tree. React Context is a useful mechanism that allows you to pass data through each child component without prop drilling. React Context can help you a lot.

**Note: using Context in some components makes them depend on that Context. Please remember that when you are architecting your app.**

## Creating Context

To create Context, you have to use react createContext method:

```javascript
export const MessagesContext = createContext();
```

## Providing data to a Context

Any Context object has its Provider component that allows passing data to the Context.

To pass data to the Provider component, you need to use value prop:

```javascript
<MyContext.Provider value={<value here>}>
```

Take a look at the real example:

```javascript
import React, { createContext, useReducer } from "react";

import {
  MessagesReducer,
  messagesInitialState,
  addMessage as addMessageAction,
  removeMessage as removeMessageAction,
} from "../../reducers/Messages";

export const MessagesContext = createContext();

export const MessagesProvider = ({ children }) => {
  const [{ messages }, dispatch] = useReducer(
    MessagesReducer,
    messagesInitialState,
  );

  const removeMessage = (message) => dispatch(removeMessageAction(message));

  const addMessage = (message) => dispatch(addMessageAction(message));

  return (
    <MessagesContext.Provider
      value={{
        messages,

        addMessage,

        removeMessage,
      }}
    >
      {children}
    </MessagesContext.Provider>
  );
};
```

That Context uses the useReducer hook for state management and returns Provider with messages array, and two methods: addMessage and remove message.

---

## Injecting Context to an App

To inject your Context into an App, you need to wrap your app by the Provider component. Typically index.js or app.js file is the best place to do this:

```javascript
import { MessagesProvider } from "./contexts/Messages";

const App = () => {
  return (
    <MessagesProvider>
              
      <Router>
                    
        <>
                          
          <PageHeader />
                          
          <Messages />
                          
          <Switch>
                                
            <Route path="/category/:categoryUrlKey" component={CategoryRoute} />
                                
            <Route path="/product/:productUrlKey" component={ProductRoute} />
                            
          </Switch>
                      
        </>
                
      </Router>
          
    </MessagesProvider>
  );
};
```

## Using React Context in components with useContext hook

React hooks enable us in functional components to store the state data. React has some hooks that are included. UseState, UseCallback, UseEffects and others. The other thing which we want to discuss in detail is useContext hook. UseContext hooks allow you to connect and consume contexts. This hook uses an argument that contains the Context of your choice. Then, you can access the context value.

The last thing I want to show you is using Context in child components.

We exported two things from the file where we declared Context:

1. MessagesContext

2. MessagesProvider

We used MessagesProvider to wrap the App component. At the same time, MessageContext references our Context, and we have to pass it as an argument to the useContext hook in the component when we want to use that Context.

```javascript
import { MessagesContext } from '../../contexts/Messages';
const Messages = () => {

    const { messages, removeMessage, addMessage } = useContext(MessagesContext);
    (...)
};
```

Now we can use all Context data in our component.

---

## Summary

React Context API provides another way to pass data to multiple components and be more precise: to all the children of Context components. The context object provides data and methods to a consumer component, and a consumer reads context value.

Alternatively, without react's Context, you can pass props down manually to each react component, but in this case, you will meet a "props drilling" problem. React's context API allows to avoid prop drilling, but on the other hand – it adds dependency between react components and Context.

Moreover, testing a react component that consumes context value is a bit more complicated, but it is, of course, double, and there are a few patterns to do that. Anyway, using Context is an option for state management in react projects instead of installing external state management libraries.

Complete set up of context API includes:

1. Create Context by using react createContext method

2. Create context provider by using the Provider react component

3. Inject context provider to the component tree

4. Consume Context in the following components by using the useContext hook
