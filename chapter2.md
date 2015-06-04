<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
####Disecting predictionIO 
## 2. Under the Hood
#### draft in progress
In the last chapter we built a simple recommendation system that suggested musical artists to users. We discovered how to load data into PredictionIO. We learned how to build a recommendation engine using that data and finally we used that engine to make recommendations. In that chapter we pretty much viewed PredictionIO as a black box. We learned some components (event server, etc), but were a bit sketchy on the details. In this chapter we are going to look under the hood and see the internal structure of PredictionIO. Our belief is that learning about the internals will help you become more skillful at using PredictionIO for your own projects. 

PredictionIO consists of a number of components.
PredictionIO integrates a number of open source software projects 

look at these in more detail

Event server we have been using is built on top of Apache HBase. 

####HBase
Apache HBase is a distributed non-relational database. If you are like most people, at any given time you work on a single computer. If you are faced with a moderate sized machine learning task, say one that involves 1TB of data, you might think that you will buy a 1tb hard drive and continue using your laptop. the problem is that it takes many hours just to read that data from the drive. It doesn't matter if you have a 16 core machine, the bottleneck is how fast you can transfer data from the drive. If you use a solid state drive things will be substantially faster but at some point (size of dataset) you will eventually want to distribute the data among machines in a cluster (aka sharding) and distribute the work of anaylyzing that data across machines as well. This is exactly what HBase was designed to do. With HBase and its underlying Hadoop Distributed File System your data can seamlessly reside on one machine, several, or thousands of machines in a cluster and distribute the analysis workload to the servers where the data is stored achieving data locality. 
Like traditional databases (MySQL, Oracle) data is stored in tables. Each row of the table represents some object and each column represents some attribute of that object. When you think of a table you probably think of a table with a fixed number of columns.  HBase is a bit different -- it is what is called a wide column store. This means that each row can have a dynamic number of columns. Another way of viewing it is as a two dimensional key-value store (like a hashtable or dictionary). It is the second most popular wide column store after Cassandra. 

You can probably already guess how PredictionIO uses HBase. **The event server** stores the data in HBase. PredictionIO has a namespace called `predictionio_eventdata` and the data for a particular app is stored in a table titled something like `events_1` which, for examples like the small one in the first chapter,  may contain 12 rows and twelve columns or for large datasets may contain  billions of rows and millions of columns. 

This distribution of work is often in the form of one or more MapReduce jobs.  In a map reduce job there are two required functions, a map function and a reduce one. The map function runs on every data object regardless of where it is in the system--to me I view it as how I want to group the data. This function typically emits two things: the key (how we want to group the data) and  The reduce function tells how to aggregate the results. Here is a very simple example. Suppose I have of cities in the U.S.


#### Apache Spark
Apache Spark is a distributed system for handling big data and performing large scale data processing including large scale machine learning. It extends the MapReduce model described above to offer a wide variety of distributed computations. In the past data scientists might have specialized applications for batch processing of data and other applications intended for interactive analysis. and another framework to handle streaming data. Spark is flexible enough to handle all these. Instead of requiring multiple computation tools, we can use just Spark.

Spark itself is a unified stack of applications. Several of these are worth noting. 

#####Spark Core
One main programming abstraction of the Spark Core is the *Resilient Distributed Dataset* or RDD. You will see this term quite frequently when we dive into the Scala code that drives PredictionIO. An RDD is an interface that describes a collection of logical records. Physically, these records might be rows in an HBase table, objects in memory, or objects in a Cassandra database. These records might be stored on one computer or a cluster of thousands of computers. The RDD is an abstraction that hides these details. To the user of Spark the data is a collection of records that can be operated on in parallel. We will learn more about RDDs throughout this book. 

The Spark Core provides


####Apache Zookeeper
As you can imagine, when you are trying to distribute work across even a small cluster of computers there is significant configuration and synchronization that needs to be done. Zookeeper provides the infrastructure for this and manages the serialization and synchronization of tasks across the cluster.  Both Spark and HBase extensively uses Zookeeper.

####ElasticSearch
Elastic Search, as the name suggests, is a search server. and it is built on Apache Lucene. a




* HBase
* ElasticSearch
* Spark

    - Spark core
    - save some details (RDD for ex.,) for later
    - or maybe bite the bullet and give a few page intro to Spark. - 
    
* Zookeeper - synchronization
* General Architecture
* Why PredictionIO?

