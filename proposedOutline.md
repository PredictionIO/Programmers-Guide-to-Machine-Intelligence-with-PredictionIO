####Proposed outline
The book would be a short (~250 page or so) book on using PredictionIO for data mining/machine learning focusing on real world applications. It will cover 3 three general data mining themes: recommendation systems, clustering systems, and classifiers. The book does not intend to offer a comprehensive discussion of all the algorithms in these areas. And it will not fully explain the theory of the algorithms. Rather, the goal is a practical one---for readers to be able to use PredictionIO on their own data to solve problems. After a few introductory chapters, each of the three themes is presented in 3 chapters. The first chapter provides an general description of the theme (for example, recommendation systems) and presents a step-by-step example of using PredictionIO  to solve a representative problem in the area. The next chapter presents several common recipes/algorithms and works through a complete example. The final chapter of each section  presents a larger real-world application, where we use a cluster of Amazon EC2 instances. This final chapter of the trio may also describe issues in deploying such systems and may end with one or more short case studies of how these systems are used. 

#####Preface - 
TBD

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




