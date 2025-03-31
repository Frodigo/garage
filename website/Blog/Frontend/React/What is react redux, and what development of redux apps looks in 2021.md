---
date: 2021-11-02
---

*last updated at 02/11/2021*

I want to invite you to the journey throughout react-redux. You will see:

- What choice of approach to state management in react apps is important?

- What is redux, and why should you use it or not?

- What are Flux architecture and event sourcing?

- What is the architecture of the typical redux app?

- How to manage side effects in the redux app?

- What are alternatives for redux-thunk middleware?

- What hooks react-redux offer?

- What is the best approach for testing redux apps?

---

## What is state management?

State management is designed to enable the exchange and use of data between different sectors. It creates a concrete data structure that represents the state of your app for you to read.

Most frameworks, including React, have a way for components to control the state. It's also helpful for applications with few components, but state management across components can quickly become a task.

That is why you need state management tools to make it easier to maintain the state. It is clear that state management becomes difficult as the app is complicated, so you require a state-management tool like Redux.

Redux is a predictable state container for JavaScript apps and offers a centralized way to manage the state. Using a framework like React, we can tell certain parts of code only to show specific values of the state.

State property updates will be automatically uploaded to the front end (if rendered there). In all, state references a condition of something at a given moment, such as whether a modal is opened or not, which data should be visible, which view is active, and so on.

---

## Why use redux?

Redux is a pattern and library for managing and updating application states using events called actions that accomplish this task by defining actions that are dispatched to reducers. All actions in an app can have a type and a payload.

Reducer accepts action and changes state depending on recipient Action Type and Payload. Reducers are pure functions and therefore are predictable.

A simple function returns the same output for the same data. In addition to communication with our application, we can subscribe to data updates. It is a simple yet elegant solution to facilitate state management for small and large applications.

---

## When to use Redux

The Redux API allows you to maintain your Apps state and keep it more predictable. The idea of adding code can seem like a bit of a chore and make complicated things look a little bit overwhelming, but that can depend on the decision-making from the architecture. If you're still unsure of who needs them, you do not. The usual scenario starts when your company's application expands to the level where maintaining the app state becomes a hassle. You are seeking to make managing the user's app straightforward. These benefits come with tradeoffs and constraints, but all of these tradeoffs come with limitations and tradeoffs, including the addition of boilerplate code.

---

## Why do I need to use React-Redux?

React Redux is the official Redux Interface Library for React. If you use Redux with any UI framework, you will generally use a library with its own internal "binding" library to put Redux together with a UI framework. Redux is a standalone library used with any UI layer or framework, including React Angular Vue Ember and Vanilla JS.

---

## Redux architecture

Let's look at the react redux architecture and what you can find in a typical redux app.

### Flux

React redux implements the Flux architecture (proposed by Facebook). The base rule of that architecture is that data flows in a single direction, and also redux state can be changed only in one place.

The other concept of Flux is that writing data is separated from reading data. It's based on the C**ommand Query Responsibility Segregation (CQRS)** design pattern.

That separation is good because typically, in apps, reading data is more frequent than writing, so it's good to separate them and scale, develop and maintain separately. Of course, sometimes using CQRS does not make sense, but it depends on projects requirements (as always)

In the Flux architecture, there are three main areas:

- **view** - that what you see and place where you can dispatch actions that can change data in a store

- **dispatcher -** receives actions and pass them to stores

- **store** - stores information

So Redux implements flux architecture in its way, and keep in mind that other tools also implement Flux but in a slightly different way. Take a look at [**MobX**](https://mobx.js.org/README.html), for example.

---

### Event sourcing & time traveling

Another idea (pattern, architecture) that react redux implements is event sourcing. That pattern is more known on the backend side. Event sourcing on the frontend in redux apps means that the state reading by the view is not the source of data.

The redux state and data are created by events (actions in react redux architecture – more information below). Typically you have a default store state, and you change that state by dispatching actions.

Thanks to that, you can build a state of what you want by triggering particular actions. Let's imagine a tester finding a bug in an app and reproducing that bug in your local environment. You can need to reproduce actions history.

Moreover, you can travel back and forth in time by performing and withdrawing specific actions and seeing the unique state for each action.

Redux has a global store and brings your component's states to one central area. The prominent place where we store the state is called a store.

That also provides an additional way for examining how a particular period an app's state changes. The store is immutable, which means it can't be directly modified. It can be cloned and replaced in place with updated properties. This cloning gives us a view of our app useful for debugging purposes, particularly in the Context of a specific app's state change.

### Redux Reducers

A reducer is only a pure function that takes two arguments and returns the current state in your app.

The first argument is the current state, and the second is an action that will modify that state. The Reducer function returns a new state based on provided current state and action.

Take a look at the example reducer:

```javascript
export function CarsReducer(state, action) {
  switch (action.type) {
    case "ADD_CAR": {
      return {
        messages: [...state.cars, action.car],
      };
    }

    case "REMOVE_CAR": {
      const indexToToRemove = state.cars.indexOf(action.car);

      if (indexToToRemove >= 0) {
        return {
          cars: [...state.cars.splice(indexToToRemove, indexToToRemove)],
        };
      }

      return state;
    }

    default: {
      return state;
    }
  }
}
```

Thar **CarsReducer** can handle two actions: *ADD_CAR* and *REMOVE_CAR.* Let's take a look at what actions are in Redux.

### Redux Actions

Actions in redux are JavaScript objects containing two features called type and payload. These actions will be used as arguments through the API method that calls Redux dispatch when an item needs dispatch. To "call" this action, we have to use a reducer in our store to update our state. We then use this function to create a new store state to preview how the app looks after actions are sent on.

Take a look at the example action creator:

```javascript
const addCar = (car) => {
  return {
    type: "ADD_CAR",
    car,
  };
};
```

Another convention is to send a car object as a field of the payload:

```javascript
const addCar = (car) => {
  return {
    type: "ADD_CAR",
    payload: {
      car,
    },
  };
};
```

Both versions are good. They are only conventions. I prefer the first one.

Those functions are called action creators because they return a plain JavaScript object (action object) that you can dispatch to the store.

---

## Redux & performance

In terms of performance in React, re-renders are something that impacts performance the most. When you use the React way to handle state, for example, hooks or even class components with private state, re render is necessary when the state is changed.

When you are integrating redux with react, the state is keeping outside react. That means the react' components read data from the redux store, and in some cases, re-renders can be unnecessary. This Is like magic, but redux can you prevent redundant re-renders OOTB.

Comparing redux performance with React Contexts, there is a vast difference. When you have a significant Context with big data objects, and there is a change in this Context, all Context's subscribers (basically children) will be re-rendered.

Of course, you can reduce redundant re-renders by using the useCallback or useMemo hooks, but you need to take care of it by yourself and write additional code.

When you use Redux and dispatch some action using the **useDispatch** hook, only components that read data changed data will re render.

That makes a difference. Of course, this does not mean that React contexts are wrong, and redux is excellent. You can manage the state efficiently both ways, and the performance typically depends on implementation (and quality).

That means the redux can help you with performance, and you should consider this when you design state management in your app.

### Collaborative UI

Another thing in terms of performance is apps that work in real-time. For example, Google docs. There you can edit documents with other users in real-time. In a case like that, Redux's architecture based on events is better because it's easier to send only events between users than sending all document data and handling change.

So using redux or not depends on the project type.

You may also ask if Redux can have a destructive impact on the performance of a react app? Sometimes - yes, but it's typically because not of redux, but because of the wrong design of an application.

React redux state is outside React, so when you design and develop a redux app, you need to decide which data should be a part of the redux store and a private state of components. Good design of state management can help to avoid performance issues.

---

## Side effects

Some actions can have side effects. For example, when you add the product to a cart, you need to display a notification. On the other hand, you can also need to work with async data. I mean, send a request for data before redux action or after.

You can manage side effects in a react component, but this is not a good idea because user action, or generally speaking an operation, is divided into two parts

1. pure - redux action - handled by reducer

2. impure - side effect - controlled by a react component

A better solution is adding one common type of place in a react app when you can handle operations. That place is called: redux middleware.

---

## Redux middleware

Redux middleware is a building block that allows you to encapsulate sending redux actions and manage side effects, async data in one place.

There are three types of redux middleware:

1. Thunks ([redux-thunk](https://github.com/reduxjs/redux-thunk))

2. Sagas ([redux-saga](https://redux-saga.js.org/))

3. Observables ([redux-observable](https://redux-observable.js.org/))

If you are developing redux apps, you should choose one of the middleware, and then Redux and middleware are responsible for the state management, and components don't need to handle side effects. Hence, they are more readable and more superficial because they only display data.

Let's go dive into each redux middleware type.

### Redux Thunk

Redux-thunks are the simplest to understand, so let's start from them! Thunks is a function that can dispatch any redux action directly to a redux store.

Moreover, you can dispatch many actions in one thunk and add additional logic of dispatching so that you can dispatch action conditionally or in a loop. Also, a thunk can call other thunks, so whatever you need, all of this is in one place.

The significant advantage of thunks is that components don't know anything about the thunk that it calls. All dependencies and logic are inside thunks, and components are only called thunk. All magic is inside.

Take a look at the example thunk:

```javascript
// redux action
function setUser(userData) {
  return {
    type: "SET_USER",
    userData,
  };
}

// redux action
function setError(errorMessage) {
  return {
    type: "SET_ERROR",
    errorMessage,
  };
}

// The thunk
function fetchUserData(userId) {
  return function (dispatch) {
    return fetch(`https://my-api.com/user/${userId}`).then(
      (data) => dispatch(setUser(data)),
      (error) => dispatch(setError(`Something went wrong... ${error}`)),
    );
  };
}
```

You can see two redux actions in the code above: setUser, setError, and the thunk named fetchUserData. That thunk receives userId as a parameter and calls [API](https://marcin-kwiatkowski.com/blog/graphql/2-ways-of-handling-graphql-errors-in-apollo-client) using fetch and then dispatch setUser action, or setError hook if the API returns error.

Take a look at another example with more logic:

```javascript
function fetchUserB2Bdata() {
  return function (dispatch, getState) {
    const user = getState().user;

    if (!user) {
      return dispatch(setError("User is not authenticated."));
    }

    if (!user.isB2Buser) {
      return dispatch(setError("User is not a B2B user."));
    }

    return fetch(`https://my-api.com/user/b2b/${user.id}`).then(
      (data) => dispatch(setUserB2Bdata(data)),
      (error) => dispatch(setError(`Something went wrong... ${error}`)),
    );
  };
}
```

As you can see, there is a getState function that allows you to get the current state and do what you need depending on it.

Those examples are elementary, and I wanted to show you (what I am writing about for a while ) the advantages of using thunks: handle async data, encapsulate actions with side effects, and async data.

### Sagas (redux-saga)

Let's take a look at the second type of redux middleware. On the homepage of redux-saga, you can read that it's "An intuitive Redux side effect manager." Let's check it's the truth! :)

Here is the example piece of code that uses redux-saga:

```javascript
import { call, put, takeEvery } from "redux-saga/effects";
import Api from "...";

// Worker saga will be fired on REQUEST_USER actions
function* fetchUserData(action) {
  try {
    const userData = yield call(Api.fetchUser, action.payload.userId);
    yield put({ type: "SET_USER", userData });
  } catch (error) {
    yield put({ type: "SET_ERROR", errorMessage: error });
  }
}

// Starts fetchUser on each dispatched REQUEST_USER action
function* mySaga() {
  yield takeEvery("REQUEST_USER", fetchUserData);
}
```

It is intuitive, isn't it?

I hope you will agree with me that at first glance, it looks more complicated than redux-thunk. Let's explain it a little bit.

The concept of redux-saga is similar to the saga design pattern. Each saga is an independent logic that is fired when some specific actions are dispatched.

In the example above, there is a **fetchUserData** saga that is fired on every **REQEST_USER** redux action.

The **takeEvery** function is a redux-saga effect. There is also the **takeLatest** effect which is fired on the latest specified redux action.

There are more effects, so you need time to understand redux-saga API. Moreover, redux-saga uses JavaScript generators that ate powerfully but also required more attention to understand them.

### Epics (redux-observable)

The last type of redux middleware which you should consider when you design a redux app is redux-observable. It's based on [RxJS](https://github.com/ReactiveX/RxJS).

In this case, redux-actions are implemented as RxJS streams, so you have a stream of actions and a stream of state. Using redux-observable, you can create **Epics** that describes connections between actions. You can think about epics like sagas from redux-saga.

For now, I don't want to go deeper with epics (and sagas as well), but you can expect separate articles about them in the future.

Summarizing – sagas and epics have a significant entry threshold, so you and your team should think twice before you decide to use them. It does not mean that they are wrong. Everything depends on a project's requirements and team credentials.

However, I will not lie if I say that redux-thunk is a good choice in 90% of cases.

---

## Modern redux with hooks

The React world can be divided into two eras: before Hooks were introduced and after Hooks were introduced.

Before, there was a connect function provided by the react redux, and you were able to map state and dispatch to props of components. Also, a connected component could give props from a parent component, so you needed to merge props from components and redux.

Writing with this method added even more redux boilerplate to your code to add child component that has access to the redux store to the component tree.

Luckily we now have hooks, and things look more straightforward.

### Hooks

React's new "hooks" API gives functions the ability to use local component states, execute side effects, and so on. React also lets us write custom hooks enabling us to extract reusable hooks to add our behavior for React's built-in hooks. React-Redux has its standard hook APIs that allow React components to subscribe to Redux stores, read state, and dispatch actions.

#### useSelector

The useSelector hook allows you to read a state from the redux store. Each call to useSelector() creates an individual subscription to the Redux store.

Take a look at the example of a react component that uses of the useSelector:

```javascript
import React from "react";
import { useSelector } from "react-redux";

export const UserDetails = () => {
  const user = useSelector((state) => state.user);
  return <h1>Hello, {user.name}</h1>;
};
```

#### useDispatch

The useDispatch hook returns a reference to the dispatch function from the Redux store. Thanks to that, you can dispatch actions in a react component as needed.

```javascript
import React from "react";
import { useDispatch } from "react-redux";

export const LogOut = ({ value }) => {
  const dispatch = useDispatch();

  return <button onClick={() => dispatch({ type: "LOG_OUT" })}>Log out</button>;
};
```

As you can see, using Redux with hooks is pretty simple, and keep in mind that it's recommended approach (instead of using connect function).

---

## Redux code boilerplate

Now let's focus on something which is a considerable disadvantage of redux - code boilerplate. When you create a new app, you set up redux and are ready to go... you need to write a lot of code: reducers, action creators. It's instead not enjoyable, more frustrating, but there is a solution for that!

### Redux toolkit

Redux toolkit is an Opinionated set of tools that can help create redux code and focus on the core logic your app needs. Thanks to that toolkit, you can write less code and do more work at the same time. Redux toolkit can help with store setup, creating reducers, immutable update logic, and more.

Take a look at the examples here: [https://redux-toolkit.js.org/tutorials/quick-start](https://redux-toolkit.js.org/tutorials/quick-start).

## Redux DevTools

Redux DevTools is a browser extension that allows you to see the status of your Redux store at any given time. It is how we can time travel by our app - as different changes take place.

If the app starts to send more actions, the software will check the user's interaction on all of its features using Redux DevTools. This is useful for debugging as your app grows, so having a running log of how your redux store state is updated will give you valuable insight into how your app ends up looking how it does.

What I like the most is inspecting actions, the current state at the moment, and time traveling. It's highly recommended to use [Redux DevTools](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en) to debug redux apps.

---

## Testing redux

Redux is simply a library that ensures we follow a particular pattern for updating our global state. Should we unit test stores, reducers, actions, and so on?

In my opinion, we shouldn't. Redux is an implementation detail, and it should be hidden in tests even when I think about redux middleware. From the perspective of a test, you don't have to use thunks, sagas, or epics. What is vital is that the state should be changed.

So I recommend testing the redux more integrally than the unit.

For example, instead of testing actions and reducers, test component that reads data and triggers actions. Test it from the user's perspective and assert that results are that as they should be.

## React Redux Tutorial for Beginners: The Complete Guide

The most simplified Redux tutorial I want when I'm figuring it out. Includes the Redux Toolbox and Redux hooks! There are many redux tutorials, but many of them are outdated, so I plan to write a new one that is up to date with approaches and techniques that we have already known in 2021. Stay tuned!

---

## Conclusion

In the end, I want to say that Redux is a complex way to manage the state in react apps and still is an option in 2021 for the state management engine for React Apps. Hooks provided by the library are effortless to use and powerful. Thanks to the redux toolkit, there is also a way to avoid a large amount of redux boilerplate code.

In some cases, Redux is a good choice, and also even if you choose Redux, you need to select other things: which middleware should I use?

Redux-thunk, redux-saga, or redux-observable?

Those middlewares can help manage side effects and asynchronous logic in different ways. Also, the level of complexity of those is different (thunks are most straightforward).

### Do I need redux?

Is another question about architecture? Do you need redux and event sourcing? Maybe alternatives as [MobX](https://mobx.js.org/README.html), [React Query,](https://react-query.tanstack.com/) or [SWR](https://swr.vercel.app/) will be better for \`you?

Moreover, Facebook is actively working on something new for state management in react apps. Check out [Recoil](https://recoiljs.org/).

### Do I migrate from redux?

The final question is, when I have the redux app, should I migrate to something else?

I was fascinated with how the redux became popular a few years ago, and I'm just as fascinated with how suddenly its popularity has declined.

When you think about migrating from redux, you need to have good reasons. Migrating because the community declines it is not a reason.

If, after a few years, it turned out that the choice of redux was not the best, it only emphasizes the importance of design and choosing the exemplary architecture for a specific project.

So, if you have reasons and money, please migrate from redux, but migrate if you want to migrate. Please give it up.
