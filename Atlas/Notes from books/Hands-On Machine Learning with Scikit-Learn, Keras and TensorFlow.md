# Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow: Concepts, Tools and Techniques to Build Inteligent Systems, 3rd Edition

ISBN: 978-83-8222-423-7

## Chapter 1: The machine learning landscape

### What is a machine learning?

Machine learning is a part of computer science that allows computers to learn from data without the need to explicitly program them.

### Four types of applications that machine learning works best for

1. Complex problems that are hard to resolve using traditional method, for example detecting spam.
2. problems that need to be tuned frequently or have a large number of rules
3. building systems that adapt to fluctuating environments
4. help people learn, example: data minning

### What is a labeled training set?

Is a data set that contains the desired solution (label) for each instance.
### What are the two most common tasks for supervised learning?

1. Classification
2. Regression

### What are the four most common tasks for unsupervised learning?

1. cluster analysis
2. anomaly detection
3. visualization algorithms
4. dimensionality reduction

### What type of algorithm would you use in a robot designed to navigate unfamiliar terrain?

I would use a reinforcement learning algorithm.

### What kind of algorithm would you use to separate customers into several different groups?

I would use cluster analysis (unsupervised learning) if I don't know what groups I want to have, otherwise I would use classification algorithm (supervised learning)

*Note: I could use one of them in NitroDigest to add tags/categories to summaries.*

### Is the spam detection problem part of a supervised or unsupervised learning mechanism?

It's a part of supervised learning because we can have a labeled training set with spam (or ham) emails that is used for learning.

### What is an online learning system?

It can learn incrrementaly. You can add new data and train model this new data. Each training step is fast and system can learn often with new data.
Oposite of this approach is a batch learning.

### What is out-of-core learning?

It's a method of training that allows to use a huge data sets that are bigger that the device memory. Process loads part of data, train the model, loads new data, train again, and repeats these steps unit all data is used for training. An out-of-core learning algorithm actually use online learning techniques to learn from partial data.

### In which algorithm is a similarity measure required to obtain predictions?

It's required in the instance-based learning algorithm. This algorithm learns the trained data by hearth and then compares each new instance to learned instances using similarity measure.

### Explain the difference a parameter and a hiperparameter of a model

Parameter describes what a model will predict given a new instance. Model can have one or more parameters. Hyperparameter is a parameter of learning algorithm itself, not a model.

### What do model learning algorithms look for? What strategy do they most often use? How do they make predictions?

Model learning algorithms typically looks for the best value for given new instance

### What are four main challenges with machine learning?

1. lack of data
2. poor data quality
3. nonrepresentative data
4. uninformative features`

### What do we have if a model performs great on the training data, but fails to generalize to new samples?

It's most likely overfitting the training data.

### What is a test set and why we need to use it?

It's a part of data that is used to check trained model. It estimate a generalization errors. We use a training set before we deploy models to production.

### What is a validation set?

It's a data set that is used to compare models and choose the best one.

### What is a train-dev set? When is needed? How we can use it?

### What are the risks when tuning a hyperparameter against the test set?

You can overfitting the test set
