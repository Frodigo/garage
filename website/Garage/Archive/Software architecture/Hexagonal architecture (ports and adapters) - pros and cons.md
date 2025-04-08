---
date: 2022-04-20
title: Hexagonal architecture (ports and adapters) - pros and cons
---
*Last updated: 20/04/2022*

Hexagonal architecture, also known as octagonal architecture or ports and adapters architecture, is an approach to software design in which business logic is isolated from the technical layer.

In hexagonal architecture, the application consists of three main parts:

1. **Ports** - interfaces that define how the application communicates with the external environment. Ports are entry and exit points of the application through which information flows.

2. **Adapters** - implementations of ports that enable communication between the application and the external environment. Adapters translate information from a format understandable by the external system to a format understandable by the application and vice versa.

3. **Business logic** - the central part of the application that processes information passed by ports and adapters. Business logic is isolated from implementation details, which enables easy interchangeability of adapters and ports without changes to the business logic.

![[hexagonal-architecture.png]]

---

## Ports

Separating business logic from infrastructure components is the main task of the hexagonal architecture. In the business logic layer, instead of directly accessing infrastructure components, you define "ports" as doors for lower-level components.

Think of these ports as USB ports. They are a socket into which you can plug something. You can plug a method for saving data into a database or save data to a file. The business logic doesn't care where the data is saved. It sends the data to the port, and what happens to the data next depends on what is "plugged" into that port.

### Adapters

An adapter is exactly what you want to plug into a port. Based on the example above, in which the business logic wants to save data, we can define such a port:

```javascript
interface Writer {
 saveData(data: string): boolean
}
```

You can see an interface that contains the **saveData** function, which takes a string argument named data and returns true or false.

Now, let's take a look at some possible adapters for this port:

```javascript
const databaseWriter: Writer = {
    saveData: (data: string): boolean => {
        console.log(`"${data}" is saved in the database...`);

        return true;
    }
}

const fileWriter: Writer = {
    saveData: (data: string): boolean => {
        console.log(`"${data}" is saved in the file...`);

        return true;
    }
}
```

Now you are defining a class that has quite an enigmatic name for the purposes of this example: **BusinessLogic**:

```javascript
class BussinesLogic {
    constructor(
        private writer: Writer
    ) {}

    execute(): void {
        this.writer.saveData('my data');
    }
}
```

The class expects to receive a **Writer** as an argument. In this simple example, the **execute** method saves the data and doesn’t care where **Writer** will save it.

Now, having defined two different adapters, you can use them as shown below:

```javascript
const app1 = new BussinesLogic(fileWriter);
app1.execute(); // "my data" is saved in the file..."

const app2 = new BussinesLogic(databaseWriter);
app2.execute(); // "my data" is saved in the database..."
```

Does this make sense?

Now let's look at a more complex example where you are creating a product page for an online store. You have the following use cases:

1. As a user, I can view information about the product and its price.

2. As a user, I can add the product to my cart.

Let's start by defining the types and interfaces for the three entities we need:

```javascript
type Price = {
    currency: string;
    amount: number;
}

interface Product {
    id: string
    getDescription(): string|null
    getPrice(): Price|null
}

interface Cart {
    addToCart(productId: string): void
}
```

Here we have the price, product, and cart. I said it would be a bit more complicated example and I think it is. :)

Now see what concrete implementation of the business logic can look like:

```javascript
class CommerceBussinesLogic {
    constructor(
        private product: Product,
        private cart: Cart
    ) {}

    execute(): void {
        this.product.getDescription();
        this.product.getPrice()
    }

    public addProductToCart(productId: string) {
        return this.cart.addToCart(productId);
    }
}
```

Business logic exposes two ports: **product** and **cart**. Now, let's write adapters for these ports. The client says that they want to integrate with the Magento eCommerce system. They say and have:

```javascript
class MagentoProductAdapter implements Product {

    private description: string|null = null;
    public price: Price|null = null;

    constructor(
        public id: string
    ) {
        console.log('Imagine that you fetch product data from ecommerce here...') // ex. fetch('<ecommerce_api_url>/product/{id}')
        this.price = {
            amount: 199.00,
            currency: 'EUR'
        }
        this.description = 'Lorem ipsum dolor sit amet';
    }

    public getDescription() {
        return this.description;
    }

     public getPrice() {
        return this.price;
    }
}

class MagentoCartAdapter implements Cart {
        private items: Array<Product>
        private subtotal: Price

    constructor() {
        console.log('Imagine that you fetch cart here ...') // ex. fetch('<ecommerce_api_url>/cart')
        this.items = []
        this.subtotal = {
            amount: 0,
            currency: 'EUR'
        }
    }

     public addToCart(productId: string) {
        console.log('addToCart clicked') // send request to eccommerce here
    }
}
```

By the way, these examples are very simple pseudo-code in TypeScript, more to show you the idea than to provide production-ready code, so if you see something like this:

```javascript
console.log("Imagine that you fetch cart here ..."); // ex. fetch('<ecommerce_api_url>/cart')
```

Now, close your eyes briefly and imagine that this code sends a request to an eCommerce system and retrieves real data. My code doesn't have imagination, so I had to hardcode some data there.

```javascript
this.items = [];
this.subtotal = {
  amount: 0,
  currency: "EUR",
};
```

Anyway - the above adapters retrieve code from eCommerce. In this case, it is Magento. See how this code can be executed:

```javascript
const myProductid = "123";
const myCommerce = new CommerceBussinesLogic(
  new MagentoProductAdapter(myProductid),
  new MagentoCartAdapter(),
);

myCommerce.execute();
// imagine that a user clicks add to cart button...
myCommerce.addProductToCart(myProductid);
```

The console prints something like this:

```javascript
[LOG]: "Imagine that you fetch product data from ecommerce here..."
[LOG]: "Imagine that you fetch cart here ..."
[LOG]: "addToCart clicked"
```

Well done, we have just written the code in Ports and Adapters architecture!

That's not all. Now imagine that after three months it turns out that your client is emotionally unstable and has decided that he want to integrate with the BigCommerce system. The business logic remains the same. What do you do?

You add adapters for BigCommerce:

```javascript
class BigCommerceProductAdapter implements Product {

    private description: string|null = null;
    public price: Price|null = null;

    constructor(
        public id: string
    ) {
        console.log('Imagine that you fetch product data from BigCommerce here...') // ex. fetch('<ecommerce_api_url>/product/{id}')
        this.price = {
            amount: 199.00,
            currency: 'EUR'
        }
        this.description = 'Lorem ipsum dolor sit amet';
    }

    public getDescription() {
        return this.description;
    }

     public getPrice() {
        return this.price;
    }
}

class BigCommerceCartAdapter implements Cart {
        private items: Array<Product>
        private subtotal: Price

    constructor() {
        console.log('Imagine that you fetch cart from BigCommerce here ...') // ex. fetch('<ecommerce_api_url>/cart')
        this.items = []
        this.subtotal = {
            amount: 0,
            currency: 'EUR'
        }
    }

     public addToCart(productId: string) {
        console.log('addToCart Bigcommerce clicked') // send request to eccommerce here
    }
}
```

And you push them into your ports:

```javascript
const bigCommerce = new CommerceBussinesLogic(
  new BigCommerceProductAdapter(myProductid),
  new BigCommerceCartAdapter(),
);
```

```javascript
bigCommerce.execute();
// imagine that a user clicks add to cart button...
bigCommerce.addProductToCart(myProductid);
```

Console says:

```javascript
[LOG]: "Imagine that you fetch product data from BigCommerce here..."
[LOG]: "Imagine that you fetch cart from BigCommerce here ..."
[LOG]: "addToCart Bigcommerce clicked"
```

---

## Infrastructure

In hexagonal architecture, the presentation layer and data access layer integrate with external components such as:

- Database

- UI

- External provider

- Message bus

### **Driving side**

The mobile application user interface code or user interface (UI) code of a web application initiates interaction with the application. User data from the UI is supported by the adapter and sent to the business logic through the port.

### **Driven side**

Even databases and external services need an application to function. In this case, the application calls an external service or sends a request to the database. Then, the adapter implements the port to be used.

---

## Dependency inversion principle

![[Dependency inversion.png]]

Dependency Inversion Principle states that high-level modules that implement business logic should not depend on low-level modules. This means that interfaces should be defined by high-level modules. This makes the system more flexible and easier to modify, because changes made in one module will not affect the other modules, as long as the interfaces remain unchanged.

---

![traditional layered architecture](layered-architecture.png)

In the layered architecture, it's exactly the opposite - higher-level modules and, frankly speaking, the core business logic that depends on lower-level modules.

The business logic is not mixed with implementation details or technological problems by inverting the dependencies.

---

## Hexagonal architecture - benefits

![business rules are not mixed with implementation details](image-8.png)

- Easy scalability

- Application development

- Easy integration with other systems

- Isolation of business logic from the technical layer, making it easier to introduce changes without affecting the entire system

**Hexagonal architecture - drawbacks**

- Increased complexity - hexagonal architecture adds components that act as intermediaries, which affects complexity

- Debugging - applications created using the hexagonal architecture pattern may be more difficult to debug because they do not directly use specific implementations.

- Translation - when the business domain is modeled independently of the database or other technology, translation between the models used for persistence or **communication** and the domain model can be inconvenient. This problem is exacerbated when the models differ significantly from each other both technically and conceptually.

- Learning curve - Hexagonal architecture differs from traditional architectural patterns, which are often imposed on developers by frameworks. This can be more difficult for new programmers due to the need for mediation, translation, and design patterns.

---

## When to use hexagonal architecture?

The correct answer is probably as always: **it depends.**

If you are building a simple CRUD application, it's probably not worth getting into ports and adapters.

The ports and adapters architecture is more suitable for complex business logic than the layered architecture.

It is worth considering the hexagonal architecture when using different external systems, frameworks, and data reading and writing methods.

You can also consider implementing only some aspects of the architecture to improve problem separation. There are many ways to do this, and it's something to discuss with your team of developers, as each project's answer may differ.

---

## Hexagonal Architecture and DDD (Domain Driven Design)

Hexagonal Architecture and **Domain Driven Design (DDD)** are two complementary approaches to software design that aim to facilitate flexibility, scalability, and ease of maintenance of various software applications and systems.

Both approaches emphasize the importance of separating business logic from the technical layer and both use interfaces to define how different parts of the system communicate with each other.

In DDD, the goal is to create a clear and consistent model of the business domain and use it to design the software system.

Hexagonal architecture allows for the introduction of this model in a flexible and scalable way, by separating business logic from implementation details and providing transparent communication interfaces.

By combining the principles of hexagonal architecture with DDD modeling techniques, it is possible to create software systems that are both flexible and easy to maintain, and perfectly tailored to the needs of the client.

**However, it is important to remember that both approaches require careful planning and design, and may not be suitable for all software projects.**

---

## Summary

Hexagonal architecture, also known as ports and adapters, is an architectural pattern that separates business logic from the technical layer and facilitates the introduction of changes without affecting the entire system.

In this pattern, the business logic exposes ports, whose implementation depends on adapters written for specific technologies. In this way, each layer is separated and can be developed independently.

Hexagonal architecture is particularly useful in complex projects that require integration with various external systems, such as databases, UI, external providers, and message buses.

The disadvantages of this architecture are increased complexity, difficulties in debugging, translation, and learning curve.

It is worth considering using hexagonal architecture in projects that require separating the business layer from implementation details and easy integration with various external systems.

You can also combine the principles of hexagonal architecture with DDD modeling techniques to create flexible, easy-to-maintain software systems that are perfectly tailored to the client's needs.

---

## Sources

[Eric Evans' Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.goodreads.com/book/show/179133.Domain_Driven_Design)

[Learning Domain-Driven Design: Aligning Software Architecture and Business Strategy - Vlad Khononov](https://www.goodreads.com/book/show/57573212-learning-domain-driven-design)

#ProgrammingFundamentals #SoftwareArchitecture #TypeScript #JavaScript #ConceptExplanation #ArchitectureReview #DeepDive #Intermediate #Microservices #Scalability
