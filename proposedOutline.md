####Proposed outline
The book would be a short (~250 page or so) book on using PredictionIO for data mining/machine learning focusing on real world applications. It will cover 3 three general data mining themes: recommendation systems, clustering systems, and classifiers. The book does not intend to offer a comprehensive discussion of all the algorithms in these areas. And it will not fully explain the theory of the algorithms. Rather, the goal is a practical one---for readers to be able to use PredictionIO on their own data to solve problems. After a few introductory chapters, each of the three themes is presented in 3 chapters. The first chapter provides an general description of the theme (for example, recommendation systems) and presents a step-by-step example of using PredictionIO  to solve a representative problem in the area. The next chapter presents several common recipes/algorithms and works through a complete example. The final chapter of each section  presents a larger real-world application, where we use a cluster of Amazon EC2 instances. This final chapter of the trio may also describe issues in deploying such systems and may end with one or more short case studies of how these systems are used. 

#####Preface - 
TBD
---

####Part 1: Introduction

---

#####Chapter 1: Getting Started w/ PredictionIO - rough draft written
######estimated page count: 20
Readers learn what PredictionIO is, how to install it on their local machine, and how to build and run a simple recommendation system. This is really a "hit the ground running" chapter -- meaning that without much explanation the readers are led through building a simple recommender.

Topics to be covered:

* a description of what a recommendation system is
* installing PredictionIO on a machine (both on a VM and cloud based)
* starting the server
* building and training a simple music recommendation system

#####Chapter 2: What is PredictionIO 
######estimated page count: 15
Readers learn about the components of PredictionIO. Why those components are important. And why they might consider using PredictionIO for their proejcts.

Topics to be covered:

* HBase
* ElasticSearch
* Spark
* Zookeeper
* General Architecture
* Why PredictionIO?

--- 

####Part 2: Recommendation Systems

---

#####Chapter 3: a closer look at recommendation systems. - rough draft written
######estimated page count: 20
Readers examine what they built in chapter 1 in more detail. They have their first peak at the engine.json file. They learn the basics of matrix factorization. They use a moderate sized dataset: the 20 million rating movieLens dataset.

Topics to be covered:

+ a look at engine.json and the 'als' entry
+ a look at how people might make recommendations based on features like 'country' or 'female vocalist'
+ matrix factorization
+ the relationship of matrices *P*, *Q*, and *R* and how we can determine one of we have the other 2.
+ a brief mention of stochastic gradient descent.
+ a look at alternating least squares (not all the details but enough to understand the algorithm)
+ using a moderate sized dataset: the 20 million rating movieLens.
+ the effect of using a different number of latent features on accuracy.
+ perhaps a look at Engine.scala or reserve that for another chapter.

##### Chapter 5. tbd
Could include discussion of other templates such as Product Ranking, E-Commerce Recommendation, Lead Scoring, Similar Product.

---

####Part 3: Classification Systems

---

#####Chapter 6: Introducing Classification
######estimated page count: 20
Readers will learn about the fundamentals of classification systems and their uses (for ex., predicting the interest of customers). Readers will implement a simple Naive Bayes classifier.

List of topics to be covered in the chapter:

+ What are classification systems?
+ Why use PredictionIO for classification?
+ a quick hands-on intro of classifiers
+ how do we measure performance of classifiers?

#####Chapter 7: Classifying text using Naive Bayes
######estimated page count: 20
Readers will learn how to handle unstructured data including how to extract features from text. They will learn the workflow of a typical classification task (training & testing)


List of topics to be covered in the chapter:

+ types of data
+ preprocessing text
+ vectorization
+ building a naive Bayes classifier
+ unning the classifier on X(20newsGroups data? ) and evaluating the results

#####Chapter 8: Classifying Big Data
######Estimated Page Count 25
Readers will learn common pitfalls of building classifiers using big data. They will learn how to run a classifier on a big data set (Wikipedia articles) on an Amazon EC2 cluster.

List of topics that will be covered in the chapter:

+	How the time and space complexity of analyzing big data grows and why PredictionIO is a good choice.
+ 	Common Pitfalls and how to work incrementally
+ step-by-step walking though of using a Naive Bayes classifier on the Wikipedia Article Database.
+ CASE STUDY TBD

---

####Part 4: Clustering Systems

---

#####Chapter 9: Jumping into Clustering
######estimated page count: 20
Readers will learn about clustering systems and their real world applications. They will learn how to build a simple k-means clustering system using PredictionIO.

List of topics to be covered in the chapter:

+ fundamentals of clustering
+ how we measure similarity
+ hands-on intro to clustering
+ the k-means clustering algorithm
+ clustering a very simple example.


#####Chapter 10:   Hierarchical Clustering and unstructured data
######estimated page count: 20
TBD

List of topics to be covered in the chapter:

+ a closer look at k-means
+ working with unstructured data - turning text into vectors
+ clustering something like the 20 news group dataset
+ possibly a discussion of canopy clustering and a hands-on exercise
+ beyond k-means
+ tentative: clusetering people on Twitter

#####Chapter 11:  Clustering big data on a cluster
######estimated page count: 20
