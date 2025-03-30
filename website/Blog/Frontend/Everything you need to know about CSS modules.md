*Date: 15/02/2021*

## CSS is easy, right?

I started my web developer journey as a frontend developer, and with time I also started to deal with backend employees. My colleagues from the backend team were laughing that CSS is just a language for just setting margins and colors.

Keep in mind: if you do something more than adding color to headings…

**CSS is not easy.**

Take a look at the list below. The biggest CSS dangers are described here:

1. Conflicts between CSS rules

2. Overwrites

3. A big CSS stylesheet with unused rules

4. Side effects

## CSS modules to the rescue

Thanks to the fact that CSS modules are scoped locally, the problems described above disappear.

- no more conflicts

- no side effects

- no global scope

## An example CSS module

Take a look below at a straightforward example of a CSS module in [PWA Studio](https://marcin-kwiatkowski.com/blog):

### CSS module (this is just a CSS file)

```css
.section {
  padding: 15px;
}

.heading {
  font-size: 24px;
  font-weight: bold;
  margin: 15px 0;
}
```

### The sample component which uses these styles

```javascript
import React from "react";
import classes from "./sample-component.css";

const SampleComponent = () => {
  return (
    <div className={classes.section}>
      <h3 className={classes.heading}>This is the sample component title</h3>
      <p>This is the sample component paragraph</p>

      <h4 className={classes.heading}>This is the sample list:</h4>
      <ul>
        <li>Sample item A</li>
        <li>Sample item B</li>
        <li>Sample item C</li>
      </ul>
    </div>
  );
};

export default SampleComponent;
```

On the third line, we imported a CSS module called sample-component.css as a classes object. Now we are able to use classes from the CSS module as object properties. Take a look at lines 6,7, and 10.

So this is exactly what CSS modules do—they let you use CSS classes as object properties in [JSX](https://marcin-kwiatkowski.com/blog/what-is-jsx-and-is-it-worth-making-friends-with-it) files.

### How does it work?

Thanks to Webpack and the configuration of the loaders, the classes described in the CSS module, and applied in the React component, are rendered as unique CSS classes for each place where they are used.

1. Here is the place where the section class is applied to the node.

2. This is a CSS rule which includes CSS properties.

3. Here you can see a unique class name applied to the node in the compiled app.

4. This is compiled into a unique CSS rule.

---

### Webpack configuration

Take a look at the webpack configuration. In PWA Studio you can find them in @magento / pwa-buildpack / lib / WebpackTools / configureWebpack / getModuleRules.js file

```javascript
getModuleRules.css = async ({ paths, hasFlag }) => ({
  test: /\.css$/,
  oneOf: [
    {
      test: [paths.src, ...hasFlag("cssModules")],
      use: [
        "style-loader",
        {
          loader: "css-loader",
          options: {
            localIdentName: "[name]-[local]-[hash:base64:3]",
            modules: true,
          },
        },
      ],
    },
    {
      include: /node_modules/,
      use: [
        "style-loader",
        {
          loader: "css-loader",
          options: {
            modules: false,
          },
        },
      ],
    },
  ],
});
```

On line 11 you can see where the names of the compiled classes come from, and line 12 is where the CSS modules are enabled.

## Composition

CSS modules let you compose rules from other rules:

```css
.heading {
  font-size: 24px;
  font-weight: bold;
  margin: 15px 0;
}

.secondaryHeading {
  composes: heading;
}
```

It’s possible to compose multiple selectors:

```css
.section {
  padding: 15px;
}

.header {
  background-color: lightgray;
}

.heading {
  font-size: 24px;
  font-weight: bold;
  margin: 15px 0;
}

.secondaryHeading {
  composes: heading;
}

.sampleHeader {
  composes: section header heading;
}
```

## Global CSS Rules

Scoping styles locally is lovely, but sometimes you need to define some global CSS rules, for example for animations (keyframes). CSS modules let us create global rules using the :global() function.

```css
// global-styles.css
:global(.global-class-name) {
  color: red;
}
```

When you import this CSS module into your app, you will be able to use a global CSS rule like this:

```javascript
// import stylesheet
import './global-styles.css'
...
// example of using global CSS rule
<p className="global-class-name">This is paragraph with global styles appiled</p>
```

### Composing from global

Sometimes it is necessary to compose from a global rule to a local one, which you can do like this:

```css
.redHeading {
  composes: global-class-name from global;
}
```

## Naming conventions

It’s recommended to use the camel case naming convention because using classes in JS, in this case, is easiest. When the name of the class looks. for example, like this: .my-sample-class, then you can apply this class to an element in the following way:

```
<ul className={classes['my-sample-class']}>
```

## Merging and overrides classes

In PWA Studio you can pass classes as props to a component, and overwrite default component classes with classes from props. Take a look:

```css
import { mergeClasses } from '@magento/venia-ui/lib/classify';
import defaultClasses from '@magento/venia-ui/lib/components/Main/main.css';

const Main = props => {
   const classes = mergeClasses(defaultClasses, props.classes);
}
```

If you pass classes as props, you can validate them using PropTypes:

```javascript
Main.propTypes = {
  classes: shape({
    page: string,
    page_masked: string,
    root: string,
    root_masked: string,
  }),
};
```

---

## Conclusion

In my opinion, locally scoped CSS resolve many problems and is a really nice, modern approach to managing styles. Perhaps for many Frontend Developers, this is a controversial approach, and that’s OK because this is completely different from what is commonly used.

Maybe you have experience with CSS modules? Let me know in the comments!

Thanks for reading. All likes, shares, and comments are really appreciated.

## Github repository

You can find examples of the code for this article on my Github.[Here is the repository.](https://github.com/Frodigo/css-modules-examples-pwa-studio)

## Sources

[https://magento.github.io/pwa-studio/technologies/basic-concepts/css-modules/](https://magento.github.io/pwa-studio/technologies/basic-concepts/css-modules/)

[https://github.com/css-modules/css-modules](https://github.com/css-modules/css-modules)

[https://webpack.js.org/loaders/css-loader/#modules](https://webpack.js.org/loaders/css-loader/#modules)

[https://x-team.com/blog/css-modules-a-new-way-to-css/](https://x-team.com/blog/css-modules-a-new-way-to-css/)

[https://glenmaddern.com/articles/css-modules](https://glenmaddern.com/articles/css-modules)
