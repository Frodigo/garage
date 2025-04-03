---
date: 2021-10-07
title: What is JSX in React, and is it worth making friends with it
---
*Last updated at 07/10/2021*

JSX is an XML/HTML-like syntax from React that extends **ECMAScript**. JSX allows you to write HTML code mixed with JavaScript. Take a look at the following example:

```javascript
export const App = () => {
  return (
    <main id="root">
      <h1>Hello Folks!</h1>
      <p>
        Random question: Is <strong>FC Barcelona</strong> win any match in the
        Champions League this season?
      </p>
    </main>
  );
};

export default App;
```

Each JSX code is converted into the React.createElement function, which the web browser knows. Take a look at the converted code I showed you in a previous snippet:

```javascript
export const App = () => {
  return React.createElement(
    "main",
    { id: "root" },
    React.createElement("h1", null, "Hello Folks!"),
    React.createElement(
      "p",
      null,
      "Random question: Is ",
      React.createElement("strong", null, "FC Barcelona"),
      " win any match in the Champions League this season?",
    ),
  );
};

export default App;
```

The react createElement function creates and returns a new React element. Here is the function signature:

```javascript
React.createElement(type, [props], [...children]);
```

The type argument can be an HTML element or React element (or even React fragment). The second argument is the props object which contains HTML tag attributes or props of a React element. The last argument is children, and so this is another jsx element transformed to React **createElement** function.

In the above code, you can see there are nested elements. All jsx tags are transported to react createElement functions, and regular javaScript can understand them.

So if you ask what is jsx in React, what is jsx meaning, I may answer you that is a special syntax that allows mixing plain JavaScript and HTML elements to speed up development. Then you can ask...

---

## Is JSX necessary for React?

It's not so if you don't like JSX syntax, or you want to write JavaScript code without configuring babel to transpioling JSX syntax to actual javascript code, you can write React apps without JSX.

Pro-tip for you then: if you want to avoid writing React.createElement too much, you can try something like this:

```javascript
const e = React.createElement;

ReactDOM.render(
  e('div', null, 'Are you sure you don't want to use JSX?'),
  document.getElementById('root')
);
```

## React JSX Explained with Examples

React JSX is React's core concept. If you have a good understanding of it properly, then you can write React code efficiently. Let's see common use cases of JSX in React.

## How do I add JavaScript code in JSX?

To add JSX-style code, you need to use curly brackets like this:

```javascript
export const App = () => {
  const welcomeMessage = "Hello folks!";

  return (
    <main id="root">
      <h1>{welcomeMessage}</h1>
    </main>
  );
};

export default App;
```

JSX doesn't allow to render objects directly as a JSX tag, so this react code is not valid, and the error occurs when using JSX Expression when rendering an object.

```javascript
export const App = () => {
  const welcomeMessage = {
    text: "Hello folks!",
  };

  return (
    <main id="root">
      <h1>{welcomeMessage}</h1>
    </main>
  );
};

export default App;
```

But you can write arrays in **JSX Expressions** because arrays are converted to strings while rendering. So this react' component is valid:

```javascript
export const App = () => {
  const welcomeMessage = ["Hello", " ", "folks", "!"];

  return (
    <main id="root">
      <h1>{welcomeMessage}</h1>
    </main>
  );
};

export default App;
```

---

## Attributes

JSX allows you to use native HTML attributes and your own custom **attributes** as well. For native HTML attributes, JSX uses camel case convention instead of the normal HTML naming convention. Besides, please note that, for example, a **class** word is a reserved keyword and **for** either. For those keywords, JSX uses a **className** for a class and a **htmlFor** for a reserved keyword (for).

## Custom HTML attributes in JSX

For custom HTML attributes, you must use a data prefix. It looks pretty the same as regular HTML.

```javascript
export const App = () => {
  const welcomeMessage = ["Hello", " ", "folks", "!"];
  const isCustom = true;

  return (
    <main id="root">
      <h1 data-isCustom={isCustom}>{welcomeMessage}</h1>
    </main>
  );
};

export default App;
```

As you can see in that react component on `<h1>` **HTML** tag, I used the data-isCustom attribute and curly braces to pass value to the attribute. Moreover, you can pass values to attributes of HTML tags using string literals like this:

```javascript
export const App = () => {
  const welcomeMessage = ["Hello", " ", "folks", "!"];

  return (
    <main id="root">
      <h1 data-mode="default">{welcomeMessage}</h1>
    </main>
  );
};

export default App;
```

---

## JavaScript Expressions

JavaScript expression may be used inside JSX. What is not surprising, I suppose, when you want to use a JavaScript expression, you need to wrap it by curly braces {}

### If statements

You cannot use **if-else** statements in JSX. Instead, you can use conditional or JavaScript ternary expressions. Take a look at the simple React component with JSX if statement:

```javascript
export const App = () => {
  const welcomeMessage = ["Hello", " ", "folks", "!"];
  const shouldDisplay = true;

  return (
    <main id="root">
      {shouldDisplay && <h1 data-mode="default">{welcomeMessage}</h1>}
    </main>
  );
};

export default App;
```

For if/else you can use something like this:

```javascript
{
  shouldDisplay ? <h1 data-mode="default">{welcomeMessage}</h1> : "no way!";
}
```

I prefer to explode JavaScript expressions to **const** (and sometimes memorize them using React useMemo hook because of performance reasons). Take a look at the JSX code below:

```javascript
export const App = (props) => {
  const { hasError } = props;
  const welcomeMessage = "Hello folks!";
  const errorMessage = "Something went wrong.";

  const shouldDisplayError = hasError ? (
    <p>{errorMessage}</p>
  ) : (
    <h1>{welcomeMessage}</h1>
  );

  return <main id="root">{shouldDisplayError}</main>;
};

export default App;
```

### Looping

When you want to render a JavaScript **array** using JSX, you can use something like this:

```javascript
export const App = () => {
  const array = ["a", "b", "c"];

  return (
    <main id="root">
      {array.map((el) => (
        <p key={el}>This is {el}</p>
      ))}
    </main>
  );
};
export default App;
```

### Spread operator

The spread operator is not supported as a child jsx expression, so you are not able to put something like this to a react component:

```javascript
 {...['a','b','c']}
```

## Comments in JSX code

If you want to insert a comment to the react component, you need to wrap its using curly braces.

```javascript
{
  /** this is comment */
}
```

---

## JSX Styling

React encourages to use of inline styles. You can use JSX expressions to pass value to the style attribute to set inline styles. React will also automatically append px following the number of the specified property.

Note: inline styling is not the only way to style react elements. There are a few other approaches, but this is the topic for another article.

---

## JSX: Conclusion

When you work on the React application, you can use JSX to put markup into javascript code. That means that you have HTML tags and JavaScript expressions in the same file.

Each JSX tag is transformed to **React createElement** javascript function. Moreover, If you don't want to use JSX for any reason, you can write react code without JSX.

In my opinion, JSX has many advantages, and definitely, it's a friend of any React developer. I love it the most in JSX because it looks like JavaScript with more power (It's fair to say that JSX is built on top of JavaScript). I like that approach more than something you can find in **Vue.js** or **Angular**, where you need to learn specific framework functions and syntax.

#WebDevelopment #FrontendDevelopment #JavaScript #React #JSX #ConceptExplanation #Tutorial #BestPractices #Intermediate