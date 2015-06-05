<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
####Disecting predictionIO 
## 2. Under the Hood
#### draft in progress
In the last chapter we built a simple recommendation system that suggested musical artists to users.  In that chapter we ignored the details focusing instead on gaining some immediate hands-on experience with PredictionIO. We learned how to load data into the event server, build a recommendation engine using that data, and deploy that engine to make recommendations.  In this chapter we are going to look under the hood and examine the internal structure of PredictionIO. We will look both at the open source projects that comprise PredictionIO and examine the basic architecture of the system.  Martin Thompson is famous for this observation:

> "Jackie Stewart, 3 times F1 world champion, coined the phrase '“'Mechanical Sympathy'”' as a term for the driver and the machine working together in harmony. This can be summarised in that a driver does not need to know how to build an engine but they need to know the fundamentals of how one works to get the best out of it."[^F1]

Martin Thompson then relates this to software developers needing to know about the underlying computer hardware. We can extend that analogy to PredictionIO. Learning about the internals will help you become more skillful at using PredictionIO for your own projects and the more we learn about the components of the PredictionIO engine the more adept we will be with getting the best out if it.

Let's look at the open source software that makes up the core of PredictionIO.

####HBase
Apache HBase is a distributed non-relational database. If you are like 99.9999% of  people, at any given time you work on a single computer. If you are faced with a moderate sized machine learning task, say one that involves 1TB of data, you might think of buying a 1TB hard drive and continuing to use your laptop. The problem with this approach is that it takes many hours just to read the data from that one drive. It doesn't matter if you have a 16 core machine, the bottleneck is how fast you can transfer data from the drive. If you use a solid state drive things will be substantially faster but at some point as the size of your dataset gets larger you will want to distribute the data among machines in a cluster (aka sharding) and distribute the work of anaylyzing that data across machines as well. This is exactly what HBase was designed to do. With HBase and its underlying Hadoop Distributed File System your data can seamlessly reside on one machine, several machines, or thousands of machines in a cluster and HBase can distribute the analysis workload to the servers where the data is stored achieving data locality. 
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

[^F1][http://www.meetup.com/skillsmatter/events/142358142/](http://www.meetup.com/skillsmatter/events/142358142/)