<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
####Disecting predictionIO 
## 2. Under the Hood
#### draft in progress
In the last chapter we built a simple recommendation system that suggested musical artists to users.  In that chapter we ignored the details focusing instead on gaining some immediate hands-on experience with PredictionIO. We learned how to load data into the event server, build a recommendation engine using that data, and deploy that engine to make recommendations.  In this chapter we are going to look under the hood and examine the internal structure of PredictionIO. We will look both at the open source projects that comprise PredictionIO and examine the basic architecture of the system.  

Martin Thompson is famous for this observation:

> "Jackie Stewart, 3 times F1 world champion, coined the phrase '“'Mechanical Sympathy'”' as a term for the driver and the machine working together in harmony. This can be summarised in that a driver does not need to know how to build an engine but they need to know the fundamentals of how one works to get the best out of it."[^F1]

He then relates this to software developers needing to know about the underlying computer hardware. We can extend that analogy to developers using pre-existing applications including PredictionIO. Learning about the internals will help us become more skillful at using PredictionIO for our own projects and the more we learn about the components of the PredictionIO engine the more adept we will be with it.

Let's look at the open source software that makes up the core of PredictionIO.

####HBase
Apache HBase is a distributed non-relational database. If you are like 99.99% of  people, at any given time you work on a single computer. If you are faced with a moderate sized machine learning task, say one that involves 1TB of data, you might think of buying a 1TB hard drive and continuing to use your laptop. The problem with this approach is that because of the physical characteristics of hard drives and computers, it takes many hours just to read the data from that one drive. It doesn't matter if you have a 16 core machine, the bottleneck will be how fast you can transfer data from the drive. If you use a solid state drive things will be substantially faster but at some point, as the size of your dataset gets larger, you will want to distribute that data among machines in a cluster (aka sharding) and also distribute the work of anaylyzing the data across machines as well. This is exactly what HBase was designed to do. With HBase and its underlying Hadoop Distributed File System your data can seamlessly reside on one machine, several machines, or thousands of machines in a cluster and HBase can distribute the analysis workload to the servers where the data is stored achieving data locality. 
Like traditional databases such as MySQL and Oracle, data is stored in tables. Each row of the table represents some object and each column represents some attribute of that object. When you think of a table you probably think of a table with a fixed number of columns sort of like this:

| -| Jake | Clara | Kelsey | Angelica | Jordyn |
|:-:|--:|--:|--:|--:|--:|
|Taylor Swift	| 5	| - 	| 5	| 2	| - |
| Purity Ring |	- |	-	| -	 | 4	| 4 |
|Father John Misty |	3 |	5 |	- | 	-	| 5 |




HBase is a bit different -- it is what is called a **wide column store**. What this means is that each row can have a dynamic number of columns. One row might have 5 columns and another, 105.  Another way of viewing a wide column store is as a two dimensional key-value store (like a hashtable or dictionary). For example, if our table is called *rating* then to retrieve any particular value from the table we need to specify both the row and the column like `rating['Taylor Swift']['Clara']`. This is a very efficient way of storing sparse datasets. Consider the table above where Jake has not rated Purity Ring. With an approach that uses a fixed number of columns, we still need to reserve a space in memory for Jake's potential rating of Purity Ring but with a wide column store we do not. With a fixed number of columns method we need to reserve space for each of the 15 cells above, but with the wide column store one we only need to reserve space for 8. This is a major benefit of wide column stores.  HBase is the second most popular wide column store after Cassandra. 

You can probably already guess how PredictionIO uses HBase. **The event server** stores the application's data in HBase. PredictionIO has a namespace called `predictionio_eventdata` and the data for a particular app is stored in a table titled something like `events_1` which, for examples like the small one in the first chapter,  may contain 12 rows and twelve columns or for large datasets may contain  billions of rows and millions of columns. 

HBase not only provides for the storage of data, it also provides an infrastructure for the distribution of work on this data in the form of one or more MapReduce jobs.  You have probably heard of the term *MapReduce*. In a MapReduce job there are two required functions, a map function and a reduce one. The map function runs on every data object regardless of its location in the cluster and typically emits two things: 

1. a key representing how we want to group the data
2. the attributes of the object we need in order to solve the problem

The reduce function tells how to aggregate the results.  Here is a very simple example. Suppose I have a dataset of cities in the U.S. Here is an example of one data object:

```
CITY
CityName: Las Cruces
State: New Mexico
Population: 101,324
Mayor: Ken Miyagishima
Elevation: 4,000
County: Dona Ana
Area: 76.31
```

And our task is to find the city with the largest population for each state. Let's say we have a long printout with this information for 30,000 cities in the U.S. and we are going to divide the task among the ten people in our group.  I'll take the sheets with the information for cities beginning with *A* and *B*, you for *C* and *D* and so on. For the map function we need to specify the key (what we want to group by) and what information we need to answer the problem. In this case we want to group by State and we need the Name of the city and Population. To solve this problem we don't need to know the mayor's name, the elevation, or any other information. Our psuedocode for the map function would be something like:

```
function mapCode
emit 
   State,
   "data": [{
           "CityName": CityName,
           "Population": Population }]

```
So for each entry in our pages of the printout, we are going to write the State, CityName, and Population on an index card and organize these index cards by state. When we are done with the map task each of us will have up to 50 piles of index cards (each pile representing a state).  Each of us is playing the role of one computer in a cluster. Now for the reduce step. Reduce operates on each key meaning that the reduce function will run on the New Mexico pile and another instance of that same reduce function will run on the California pile. What do we want reduce to do in this example?  Well, we want it to go through each pile and find the city with the largest population. So instead of 50 piles of cards I will now have 50 cards, each card representing the largest city in that state's pile of what once was a pile of city cards. 

```
function reduceCode(key, data)
  return maximum value in data
```

Remember the there are ten of us working on this problem and each of us might have a pile of one card representing the largest city in New Mexico. I might have Cloudcroft with a population of 674, you might have Las Cruces with a population of 101,324, and our friend Ann might have Albuquerque with a population of 903,000. So we need to work together and apply reduce again across our friends (across machines in a cluster) and apply it again if necessary, until we only have one set of largest cities among us. 

This concept of MapReduce is amazingly cool because it gave developers critical insights into how to develop distributed applications in a somewhat easy manner. When you spent your life developing applications that run on one machine, it is conceptually very difficult to transition to writing applications for a cluster of machines. Here is where MapReduce played a pivotal role. It was instrumental in moving the software development community toward developing applications for clusters. 



#### Apache Spark
Apache Spark is a distributed system for handling big data and performing large scale data processing including large scale machine learning. It extends the MapReduce model described above to offer a wide variety of distributed computations. In the past, data scientists might have specialized applications for batch processing of data and other applications intended for interactive analysis and another framework to handle streaming data. Spark is flexible enough to handle all these. Instead of requiring multiple computation tools, we can use just Spark.

Spark itself is a unified stack of applications. Several of these are worth noting. 

#####Spark Core
The Spark Core provides an API that provides a layer of abstraction over such implementation details as how the data is stored. 
One main programming abstraction of the Spark Core is the *Resilient Distributed Dataset* or RDD. You will see this term quite frequently when we dive into the Scala code that drives PredictionIO. An RDD is an interface that describes a collection of logical records. Physically, these records might be rows in an HBase table, objects in memory, or objects in a Cassandra database. These records might be stored on one computer or a cluster of thousands of computers. The RDD is an abstraction that hides these details. To the user of Spark the data is a collection of records that can be operated on in parallel. We will learn more about RDDs throughout this book. 

The Spark Core also contains components for handling scheduling, fault recovery, and a range of other tasks. For example, when you use Spark you can assign a static number of CPU cores to a particular application, or you can  have Spark dynamically share CPU cores among applications. This later allocation might be useful if you are running a number of interactive Spark sessions where each sessions does not overly task the CPU core. This is all handled by the Spark Core.

#####MLlib
MLlib is the machine learning library containing a wide range of machine learning algorithms. These include algorithms for classification, regression, recommendation, and clustering. PredictionIO makes heavy use of this library, but we should mention that in using PredictionIO you are not limited to just the algorithms provided by MLlib. 

####ElasticSearch
Apache Lucene is a text search/information retrieval software library. It reads and indexes text and provides an extensive API for search that index. It has been tuned for speed particularly with large datasets. It's used by a variety of companies including those with heavily-trafficked websites such as Disney, Ticketmaster and Twitter. **ElasticSearch**, as the name suggests, is a search server and it is built upon Apache Lucene.  In addition to other services, it provides an easy-to-use wrapper around Lucene. ElasticSearch is distributed and the indices it creates can be divided among a number of computers in a cluster.

ElasticSearch is used in a number of ways in PredictionIO most of which deal with the storage of metadata such as version control of models and engines, and evaluation results.

####Apache Zookeeper
As you can imagine, when you are trying to distribute work across even a small cluster of computers there is significant configuration and synchronization that needs to be done. Zookeeper provides the infrastructure for this and manages the serialization and synchronization of tasks across the cluster.  Both Spark and HBase extensively uses Zookeeper.


### The DASE Architecture
The developers have designed PredictionIO based on what they call the DASE architecture. This architecture defines the four components you need to specify to create a PredictionIO machine learning engine: the **D**ata source and data preparator, the machine learning **A**lgorithm, the **S**erving component which responds to queries, and the **E**valuation metrics.  The execution flow is something like this:

![Alt text](http://guidetodatamining.com/markdownPics/DASEarchitecture.png)

When we download and build an engine there is a bit of Scala code that specifies each of these components. When we build our recommendation system in the previous chapter we merrily ignored this code and used the default implementation. Starting with the next chapter we will start our gradual dive into learning how to refine these DASE components to better fit the particular application we are building. As a preface to that hands-on work, let us briefly examine each of these components. 

####The Data Source and Data Preparator
Typically, the data for your machine learning engine is stored in HBase as described above and that data is represented as a two dimensional hash table a bit like this

```
ROW   COLUMN     VALUE
7F2   e:e        rate
7F2   e:eid      Jake
7F2   e:ety      User
7F2   e:p        {"rating":5.0}
7F2   e:teid     Taylor Swift
8CE   e:e        rate
8CE   e:eid      Clara
8CE   e:ety      User
8CE   e:p        {"rating":3.0}
8CE   e:teid     Miranda Lambert

```


As we have learned Spark's machine learning algorithms use the Resilient Distributed Dataset or RDD. The Data Source and Preparator create an RDD that is amenable to processing by the Spark machine learning algorithms.   When we use a default engine, this PredictionIO code is already provided for us.

####The Algorithm
We also need to specify what machine learning algorithm to use and any parameters that algorithm requires. In the recommendation system we built in the previous chapter we used the default Alternating Least Squares, algorithm—an algorithm we will learn more about in the next chapter. The default Scala code also specified several parameters used by that algorithm. PredictionIO provides a number of key machine learning algorithms. You can use these as-is, modify them, or build an algorithm from scratch. We will learn more about each of these options in subsequent chapters. A PredictionIO machine learning engine may use multiple algorithms and combine the results. 

Once we define the data source and preparator, and one or more algorithms we can train the engine, building what is called a predictive model.

The algorithm also specfies how to handle prediction requests. Typically the algorithm received a query, processes that query and produces a list of predicted results. 

####Serving
Once the algorithm produces a list of results, the serving component converts these to JSON and returns the final predicted results. The default serving component does exactly this. However you can modify the behavior in a number of ways. For example, if there are multiple algorithms, the serving component can combine the results of these algorithms. On ocasion you may want to filter the results. For example, if you are recommending products you may not want to show out-of-stock items.

####Evaluation
The Evaluation component of an engine evaluates the accuracy of the engine by comparing the actual results to the predicted results. This is particularly useful if you want to tune your engine by adjusting a variety of parameters. The evaluation module can repeatedly adjust the parameters  and evaluate to find the parameter values that produce the most accurate results. 


[^F1][http://www.meetup.com/skillsmatter/events/142358142/](http://www.meetup.com/skillsmatter/events/142358142/)