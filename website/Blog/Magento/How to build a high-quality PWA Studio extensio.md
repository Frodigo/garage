---
date: 2023-02-11
title: How to build a high-quality PWA Studio extensio
---
*Published at: 2023-02-11*

First, we need to set up our local PWA Studio instance.

```bash
yarn create @magento/pwa
```

It would be best if you answered some questions on the console.

Then please generate a unique, secure, custom domain for your new project.

```bash
cd <PWA Studio root directory>>
yarn run buildpack create-custom-origin .
```

---

## Scaffolding extension

For development, I recommend creating a module in the *pwa-studio-root*/src directory and linking it as symlinks in package.json.

```bash
cd src/
yarn create @larsroettig/pwa-extension
```

Again, you will have to answer a few questions.

---

Now we need to link our module in the package.json file. Please add this entry as a dependency:

```json
"@marcinkwiatkowski/account-information": "link:<absolute_path_to_module"
```

Now we need to install our module and run the PWA Studio instance.

```bash
yarn install
yarn run watch
```

Before we start development, we should do four things:

- add @magento/venia-ui as a peer dependency

- add @magento/peregrine as a peer dependency

- run the yarn install command in our module directory

- drink coffee, water, or whatever you like

## A few words about the extension

Today we will create an account information page where Customers will find the necessary information about themselves.

### Requirements

1. The Page should be visible at the ‘base_url/account-information’ URL

   1. the Page should be visible only for logged-in customers
   2. the Customer’s first name and last name will be displayed on the Page.

2. A link to the Page should be visible in the customer menu

---

## Adding a new route

Now it’s time to coding!

### Defining the route

Thanks to targets, we can add a new route to PWA Studio in an easy way. Please add the following content to the intercept.js file:

```javascript
targets.of("@magento/venia-ui").routes.tap((routes) => {
  routes.push({
    name: "AccountInformation",
    pattern: "/account-information",
    path: require.resolve(
      "@marcinkwiatkowski/account-information/src/lib/components/AccountInformation/",
    ),
  });
  return routes;
});
```

As you can see on line 6, we defined the component which will be rendered when the user opens the Page.

### Adding AccountInformation component

To start, please create a straightforward React component:

```javascript
import React from "react";

const AccountInformation = () => {
  return (
    <div>
      <h1>Hello world</h1>
    </div>
  );
};

export default AccountInformation;
```

## Remember to add an index.js file, which exports the component

## Adding customer data

We need to have three pieces of information about the Customer:

1. Is the Customer signed in?

2. First name

3. Last name

We are going to create the hook which will use the useUserContext talon. Please create a file at **src / lib / talons / AccountInformation / useAccountInformation.js** with the following content:

```javascript
import { useUserContext } from "@magento/peregrine/lib/context/user";

/**
 * useAccountInformation hook which provides data for AccountInformation component
 * @returns {{currentUser: {id, email, firstname, lastname, is_subscribed}, isSignedIn: boolean}}
 */
export const useAccountInformation = () => {
  const [{ currentUser, isSignedIn }] = useUserContext();

  return {
    currentUser,
    isSignedIn,
  };
};
```

---

## Display information about Customer on the Page

To display the Customer’s information, we have to import the hook and add JSX Markup to the component:

```javascript
import React from "react";
import { useAccountInformation } from "../../talons/AccountInformation/useAccountInformation";

const AccountInformation = () => {
  const { currentUser, isSignedIn } = useAccountInformation();

  return (
    <div>
      <h1>Account information</h1>

      <ul>
        <li>
          <strong>First name: </strong>
          <span>{currentUser.firstname}</span>
        </li>
        <li>
          <strong>Last name: </strong>
          <span>{currentUser.lastname}</span>
        </li>
      </ul>
    </div>
  );
};

export default AccountInformation;
```

---

## Adding styles

The next thing which we do is to add styles for our component. Please create the *accountInformation.css* file in the component directory:

```css
.root {
  display: grid;
  padding: 2.5rem 3rem;
  row-gap: 2rem;
}

.title {
  justify-self: center;
  font-family: var(--venia-global-fontFamily-serif);
  font-weight: var(--venia-global-fontWeight-bold);
}

.list {
  justify-self: center;
  margin: 15px auto;
  text-align: center;
}
```

Then you can import these styles as a module component and use them.

```javascript
import React from "react";
import { useAccountInformation } from "../../talons/AccountInformation/useAccountInformation";
import { mergeClasses } from "@magento/venia-ui/lib/classify";
import defaultClasses from "./accountInformation.css";

const AccountInformation = (props) => {
  const classes = mergeClasses(defaultClasses, props.classes);
  const { currentUser, isSignedIn } = useAccountInformation();

  return (
    <div className={classes.root}>
      <h1 className={classes.title}>Account information</h1>

      <ul className={classes.list}>
        <li>
          <strong>First name: </strong>
          <span>{currentUser.firstname}</span>
        </li>
        <li>
          <strong>Last name: </strong>
          <span>{currentUser.lastname}</span>
        </li>
      </ul>
    </div>
  );
};

export default AccountInformation;
```

---

## Checking if the Customer is logged in

We want to redirect to the homepage when the Customer is not logged in. To achieve this, we are going to use the @magento/venia-drivers Redirect component.

```javascript
import React from "react";
import { useAccountInformation } from "../../talons/AccountInformation/useAccountInformation";
import { Redirect } from "@magento/venia-ui/lib/drivers";
import { mergeClasses } from "@magento/venia-ui/lib/classify";
import defaultClasses from "./accountInformation.css";

const AccountInformation = (props) => {
  const classes = mergeClasses(defaultClasses, props.classes);
  const { currentUser, isSignedIn } = useAccountInformation();

  if (!isSignedIn) {
    return <Redirect to="/" />;
  }

  return (
    <div className={classes.root}>
      <h1 className={classes.title}>Account information</h1>

      <ul className={classes.list}>
        <li>
          <strong>First name: </strong>
          <span>{currentUser.firstname}</span>
        </li>
        <li>
          <strong>Last name: </strong>
          <span>{currentUser.lastname}</span>
        </li>
      </ul>
    </div>
  );
};

export default AccountInformation;
```

---

## Adding a link to the customer menu

The Page looks good, but Customers need to know that this Page exists, so we will add a \\ link to the customer menu. If the user clicks the link, PWA Studio will redirect to the account-information Page.

Note: I’m using overwrites here to extend the VeniaUI component and overwrite talon, but in the next version of PWA Studio, there will be a better way to extend talons using a new called Targetables.

---

## Overwriting components

Create the file **lib / components / AccountMenu / accountMenuItems.js**

```javascript
import React from "react";
import { func, shape, string } from "prop-types";
import { FormattedMessage } from "react-intl";

import { Link } from "@magento/venia-drivers";
import { mergeClasses } from "@magento/venia-ui/lib/classify";
import { useAccountMenuItems } from "../../talons/AccountMenu/useAccountMenuItems";

import defaultClasses from "@magento/venia-ui/lib/components/AccountMenu/accountMenuItems.css";

const AccountMenuItems = (props) => {
  const { onSignOut } = props;

  const talonProps = useAccountMenuItems({ onSignOut });
  const { handleSignOut, menuItems } = talonProps;

  const classes = mergeClasses(defaultClasses, props.classes);

  const menu = menuItems.map((item) => {
    return (
      <Link className={classes.link} key={item.name} to={item.url}>
        <FormattedMessage id={item.id} />
      </Link>
    );
  });

  return (
    <div className={classes.root}>
      {menu}
      <button className={classes.signOut} onClick={handleSignOut} type="button">
        <FormattedMessage id={`Sign Out`} />
      </button>
    </div>
  );
};

export default AccountMenuItems;

AccountMenuItems.propTypes = {
  classes: shape({
    link: string,
    signOut: string,
  }),
  onSignOut: func,
};
```

The most important thing here is line 7 where we change the path to the useAccountMenuItems talons.

The next thing we need is the lib / talons / AccountInformation / useAccountInformation.js talon.

```javascript
import { useCallback } from "react";

/**
 * @param {Object}      props
 * @param {Function}    props.onSignOut - A function to call when sign out occurs.
 *
 * @returns {Object}    result
 * @returns {Function}  result.handleSignOut - The function to handle sign out actions.
 */
export const useAccountMenuItems = (props) => {
  const { onSignOut } = props;

  const handleSignOut = useCallback(() => {
    onSignOut();
  }, [onSignOut]);

  const MENU_ITEMS = [
    {
      name: "Communications",
      id: "accountMenu.communicationsLink",
      url: "/communications",
    },
    {
      name: "Account Information",
      id: "accountMenu.accountInfoLink",
      url: "/account-information",
    },
  ];

  return {
    handleSignOut,
    menuItems: MENU_ITEMS,
  };
};
```

The last thing is to add **moduleOverrideebpackPlugin**, add a mapping, and modify the intercept.js file.

**I’ll let you handle this one!**

If you do it correctly, you will see a link to the Page in the menu:

---

## Unit tests

Thanks to the generator, we have already configured the environment for unit tests. We can use the Jest Testing Framework.

Please add a **src / lib / components / AccountInformation / \_\_tests\_\_/ AccountInformation.spec.js** file with the following content:

```javascript
import React from "react";
import { default as createTestInstance } from "@magento/peregrine/lib/util/createTestInstance";
import { useAccountInformation } from "../../../talons/AccountInformation/useAccountInformation";
import AccountInformation from "../AccountInformation";

jest.mock(
  "@marcinkwiatkowski/customer-menu/src/lib/talons/AccountInformation/useAccountInformation",
);
jest.mock("@magento/venia-ui/lib/classify");
jest.mock("@magento/peregrine/lib/context/user", () => {
  const userState = {
    isGettingDetails: false,
    getDetailsError: null,
  };
  const userApi = {
    getUserDetails: jest.fn(),
    setToken: jest.fn(),
    signIn: jest.fn(),
  };
  const useUserContext = jest.fn(() => [userState, userApi]);

  return { useUserContext };
});

jest.mock("@magento/venia-ui/lib/drivers", () => ({
  Redirect: (props) => <mock-Redirect {...props} />,
}));

test("Redirects when not authenticated", () => {
  useAccountInformation.mockReturnValue({
    isSignedIn: false,
    currentUser: null,
  });

  const tree = createTestInstance(<AccountInformation />);
  expect(tree.toJSON()).toMatchSnapshot();
});

test("Display page when user is signed in", () => {
  useAccountInformation.mockReturnValue({
    isSignedIn: true,
    currentUser: {
      firstname: "Marcin",
      lastname: "Kwiatkowski",
    },
  });

  const tree = createTestInstance(<AccountInformation />);
  expect(tree.toJSON()).toMatchSnapshot();
});
```

### Running tests

If you want to run a test, just run this command:

```bash
yarn run test
```

The results should look like this:

## Other generator features

The generator has a few other features which help you to create excellent quality components.

### Linting

**ESLint checks all JavaScript code.** You can run this linter manually using this command:

```bash
yarn run lint
```

Configuration for esLint is in the **.eslintrc.js** file.

### Code formatting

Also, you can automatically format your code by running this command:

```bash
yarn run format
```

### Husky

Thanks to Husky, these commands (lint and format) run automatically before each git commit.

---

## Source code

You can find the source code of the extension which we just made on my [Github.](https://github.com/Frodigo/pwa-studio-extension-example)

---

## Summary

As you can see, thanks to **PWA Studio Extension Generator**, you can start developing your extension quickly, and you don’t have to worry about configuring things from scratch. You can grab base files and configs and change whatever you want. Happy Hacking!

#WebDevelopment #FrontendDevelopment #ProgrammingFundamentals #JavaScript #CSS #Bash #React #PWAStudio #Jest #Yarn #GraphQL #Tutorial #ProjectSetup #BestPractices #Intermediate #Testing