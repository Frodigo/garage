---
date: 2021-03-25
title: How to extend PWA Studio with new features
---
*Published at 25/03/2021*

This time I would like to show you how to extend **PWA Studio** with new features. After reading you will know the following:

- What is the **PWA Studio’s extensibility framework** and what tools/techniques it offers

- How to extend the PWA Studio storefront

- How to create a new PWA Studio module

- How to customize PWA Studio storefront’s styles

---

## PWA Studio extensibility framework

PWA Studio extensibility framework is a set of tools that helps developers to extend storefronts in a smart way.

What does that mean? For me extension is smarty if it adds something to the app without core code overwriting, for example:

- adding a new payment method without overwriting any checkout core files - this is smart

- adding a short description to a product page without overwriting a bunch of components including the product root component - this is also cute

- to overwrite the JS and CSS file of one of the components to change the look of it - this is totally thoughtless

Overwriting core files causes unexpected errors and complicates a project. Each overwrite complicates everything more and more and whatever you want to do in the project with a huge amount of overwrites is hard to do.

if you had overwritten too much in your project you would have looked like the guy on the image.

Thanks to the PWA Studio extensibility framework you can minimize the amount of overwriting to a minimum.

**Note:** We are talking about PWA Studio 9 introduced targetables. Thanks to this, extending PWA Studio with the new features is possible without overwriting core code. In previous versions of PWA Studio, it was not possible in general, and keep in mind that many of my articles and tutorials are deprecated now and I need to update them.

---

## Targets

One of the options to extend PWA Studio is to use Targets.

**How it works:**

- Using interceptor pattern to modify core behavior by modifying core code output during build time.

- the point that you can intercept the normal logic is Targets

- targets are variants of a JavaScript pattern called Tappable hook

- targets share some functionality with NodeJS’s EventEmitter class

---

## TargetProviders

The TargetProvider is an object that provides public API to create targets and intercepting targets from other extensions.

For example, you can use routes Targets to add a new route. In this case, you create an intercept.js file in use "routes" target to add a new route to your storefront.

```javascript
// intercept.js
module.exports = targets => {
    const veniaTargets = targets.of('@magento/venia-ui');
    const routes = veniaTargets.routes;

    routes.tap(
      routesArray => {
         routesArray.push({
             name: 'New route',
             pattern: '/new-route',
             path: '@organization/module'
         });
         return routesArray;
      })
}

// package.json
{
  "pwa-studio": {
    "targets": {
      "intercept": "intercept.js"
    }
  }
}
```

---

## Targetables

Another method to customize PWA Studio is using targetables which are object which represents source files in your projects.

Thanks to targetables you can for example get a specific component and insert JSX wherever you want. Take a look at the example below:

```javascript
const { Targetables } = require("@magento/pwa-buildpack");

module.exports = (targets) => {
  const targetables = Targetables.using(targets);

  const MainComponent = targetables.reactComponent(
    "@magento/venia-ui/lib/components/Header/header.js",
  );

  MainComponent.insertAfterJSX("<MegaMenu />", "<div>My new section!!</div>");
};
```

On the other hand, if you create your own PWA Studio extension you can use Targetqables to add specific targets for other modules.

---

## How to customize PWA Studio

Typically if you deal with PWA Studio you create a new Storefront or a new extension.

### Creating a new storefront

The first option to extend PWA Studio with new features is by creating a new storefront. Venia concept can be your starting point, but it’s not obligatory. Typically you will start from the Venia concept because it has many excellent features already implemented. In this case, you start by scaffolding your project using the `yarn create @magento/pwa` command. Then you have the opportunity to add customizations.

Take a look at an example scenario when you want to add a new section to the product page. Let’s add lorem ipsum text before *Add to cart* button.

First, scaffold the PWA Studio project:

```bash
yarn create @magento/pwa
cd <project_dir>
yarn run buildpack create-custom-origin
yarn run watch
```

Second, add this code to the `local-intercept.js` file:

```javascript
const { Targetables } = require("@magento/pwa-buildpack");

module.exports = (targets) => {
  const targetables = Targetables.using(targets);

  const ProductFullDetailComponent = targetables.reactComponent(
    "@magento/venia-ui/lib/components/ProductFullDetail/productFullDetail.js",
  );

  ProductFullDetailComponent.insertBeforeJSX(
    '<Button type="submit" />',
    "<span>Hello World! </span>",
  );
};
```

This code inserts a span with Hello World! Before submit button of the add to cart form.

#### Targetables public API

In the example above, I used `insertBeforeJSX` method of`@magento / pwa-buildpack / lib / WebpackTools / targetables / TargetableReactComponent.js`

There are a few more public methods available that help you with modifying the PWA Studio storefront:

- **insertAfterJSX** - Inserting a JSX element \_after\_ \`element\`.

- **addJSXClassName** - Adding a CSS classname to a [JSX](https://marcin-kwiatkowski.com/blog/what-is-jsx-and-is-it-worth-making-friends-with-it) element.

- **addReactLazyImport** - Add a new named dynamic import of another React component

- **appendJSX** - Appending a JSX element to the children of \`element\`

- **prependJSX** - Prepending a JSX element to the children of \`element\`.

- **removeJSX** - Removing the JSX node matched by 'element'.

- **removeJSXProps** - Removing JSX props from the element if they match one of the lists of names.

- **replaceJSX** - Replacing a JSX element with a different code.

- **setJSXProps** - Setting JSX props on a JSX element.

- **surroundJSX** - wrapping a JSX element in an outer element.

As you can see, those JSX manipulations are powerful and let you do whatever you want.

### Creating a new extension

Another way to customize PWA Studio is by creating a new extension. For example, if you had wanted to add integration with any headless CMS systems, you would have to create a new extension.

Everyone who wants to use your extension can install it and use it in his project. This also means that any extension can be extended in storefronts where it’s used.

As an extension creator, you can use Targetables in your intercept file to add specific Targets that are available to other extensions.

I recommend using [PWA Studio extension generator](https://github.com/larsroettig/create-pwa-studio-extension) to create new PWA Studio extensions.

You can create an extension using one command:

`$ yarn create @larsroettig/pwa-extension`

Then you need to link your extension in the package.json file of the PWA Studio project and you can work on it.

If you want to read more about creating extensions please check [this article.](https://marcin-kwiatkowski.com/how-to-build-a-high-quality-pwa-studio-extension)

### Styling PWA Studio

The common thing that frontend developers do is styling. In terms if you want to customize styles of the Storefront you need to add your custom styles somewhere.

Thanks to Targetables styling PWA Studio is much more simplified than before. Chris Brabender wrote a fascinating article about this.

You can find it here: [https://dev.to/chrisbrabender/simplifying-styling-in-pwa-studio-1ki1](https://dev.to/chrisbrabender/simplifying-styling-in-pwa-studio-1ki1)

---

## Summary

Since PWA Studio 9.0.0 developer experience is much better, there is a public API called Targetables that gives developers an easy way to customize PWA Studio Storefronts.

Thanks to that, you can manipulate JSX output and develop high-quality storefronts/extensions.

Besides that, there is the Targets API that allows, for example, to create a new storefront routes or new content renderers in 1 minute without any overwrites.

All of these goods make PWA Studio a great starting point for any new headless projects connected with the Magento backend.

---

## Sources

- [https://magento.github.io/pwa-studio/pwa-buildpack/extensibility-framework/](https://magento.github.io/pwa-studio/pwa-buildpack/extensibility-framework/)

- [https://en.wikipedia.org/wiki/Interceptor_pattern](https://en.wikipedia.org/wiki/Interceptor_pattern)

- [https://github.com/webpack/tapable](https://github.com/webpack/tapable)

- [https://magento.github.io/pwa-studio/venia-ui/reference/targets/#routes--tapableasyncserieswaterfall](https://magento.github.io/pwa-studio/venia-ui/reference/targets/#routes--tapableasyncserieswaterfall)

#WebDevelopment #FrontendDevelopment #JavaScript #JSX #React #PWAStudio #Magento #Webpack #ConceptExplanation #Tutorial #BestPractices #Intermediate #Extensibility #CustomizationTechniques
