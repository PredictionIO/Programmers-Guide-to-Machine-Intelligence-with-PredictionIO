###Lesson 1: Getting Started with PredictionIO
# a recommender
#### very rough draft - just testing markdown


Suppose we want to develop a web app the recommends musical groups to people. People rate the artists they like on a scale of 1 to 5 (5 being they really like them) and based on these ratings our system will make a recommendation.  Let’s say we have a small dataset that looks like this.

| | Jake | Clara | Kelsey | Angelica | Jordyn |
|:-:|--:|--:|--:|--:|--:|
|Taylor Swift	| 5	| - 	| 5	| 2	| - |
|Miranda Lambert |	- |	-	| 5 |	2 | 	- |
| Brad Paisley	| 5	| - |	5	| 1	| 1 |
| Purity Ringl |	- |	-	| -	 | 4	| 4 |
|Father John Misty |	3 |	5 |	3 | 	-	| 5 |
|Nicki Minaj |	-	| - | 	1	| 4 |	5 |
| Ed Sheeran	| 3 |	3	| 3 | 	- |	- |
| Ariana Grande |  	- |	- |	-	| 5 |	- |
| Flying Lotus |	-	| 4	| - | 3 | 	- |
| Thundercat |	1	| 4	| - | -	 |1 |

The hyphen in the chart indicates the user hasn’t rated that item. So when we make a recommendation we will select one of these hyphenated items. So, for example, for Jake we are going to select a recommendation from among Miranda Lambert, Purity Ring, Nicki Minaj, Ariana Grande, and Flying Lotus. We are going to base our recommendation on the type of music Jake likes and doesn’t like.



> ####What do you think?
> I imagine some of you were reading along, encountered the table,  glanced it it thinking “yep, a table, artists, people, some ratings” and then continued reading. That’s fine. I skim things all the time. But to get a deep understanding of the task we need to pause and engage our brain. That’s a picture of our friend Jake there on the right and we truly want to recommend something to him. Take another look at that table and see what you would recommend to him. It may help to write your answers down on a piece of paper--further engaging your brain.



  




For this small data set we can do the job pretty well by hand--we can just eyeball the table and make our recommendations quickly. Great. So we develop a web app that lets people rate artists. We hire a guy who looks at a user’s ratings, consults the above table and makes recommendations. Sounds like a great business plan. But suppose we have lots more data. Instead of ten artists we have thousands and instead of five users we have five hundred. And suppose the data is constantly changing--users are regularly entering new ratings. Here the guy-in-the-back-room approach won’t scale and we look to automate the process. We can task a developer to write a recommendation system from scratch by hand, or we can turn to a pre-existing open-source solution like PredictionIO. 

![Alt text](http://guidetodatamining.com/markdownPics/programming1.png)
![Alt text](http://guidetodatamining.com/markdownPics/programming2.png)
 We have the common problem of scalability.  The popularity of our web app took off and now we have tens of thousands of users and information on tens of thousands of musical artists. We can no longer store the data on a single machine so we need to distribute the data across a cluster of computers. With this amount of data, running our home-built recommendation software on a single machine is too slow.   So now we are faced with the daunting task of writing a distributed application that accesses a distributed data set and you need to handle synchronization among all these components. Eeeks. 
 

Before diving too deeply into predictionIO let’s get our hands dirty and see how we can implement the above recommendation task in it.

### Preliminary steps
#### step i installing the software
Before we start developing our recommendation system we need to install the predictionIO stack of software. There are a number of installation options:

* If you have a Mac or Linux machine, you can install PredictionIO directly on your machine.
* You can use an Amazon AWS EC2 instance.
* You can use a terminal.com snapshot image
* You can install it on your Windows, Mac, or Linux machine under Vagrant (so PredictionIO is running in a virtual machine).
* You can install it in a Docker Container and run it locally.
So how do you chose which is right for you?  Here are my opinions.

If you have less than 8GB memory on your machine, use either Amazon EC2 or terminal.com.   PredictionIO seems to work best with at least 2GB of memory so running it in a virtual machine (using, for example, Vagrant or Docker) on a laptop/desktop that has less than 8GB memory is iffy. This statement is probably fairly noncontroversial. Now on to my highly personal opinions. 
If you just want to explore PredictionIO I would not install it directly on a Mac or Linux machine. Why not? First a disclaimer then two reasons not to. The disclaimer. I have never, ever installed PredictionIO directly on my Mac or Linux box. It may be the most wonderful experience ever and I am missing out on this. My recommendation is based on my experience installing other software directly. 

#### Hassle 1
Suppose I want to install the Moses Statistical Machine Translation Toolkit on a Linux machine. I run into install problems which I can’t decipher. I google for an hour and discover that I have version 5.1 of some tool and the Moses installer assumes I have version 4.3. Or it does install but I am getting errors due to some subtle difference between my machine and the ones the Moses developers use. Installing software in a virtual machine under Vagrant or Docker drastically reduces the likelihood of these inconsistencies.   

#### Hassle 2
The other hassle is if I install something, Moses say, and decide it isn’t for me, I would like to delete every bit of it from my system and return the system back to its pre-Moses state. With software with multiple components that is sometimes hard to do.  If I installed software using a vagrant box (a virtual machine) or Docker container  I can simply delete the virtual machine and my laptop is back to its pristine state. both those problems go away. 
 Again, these are my opinions. If you have a Mac or Linux machine with less than 8GB you could install it directly.
The predictionIO website contains detailed instructions for installing the software in a variety of contexts on the page http://docs.prediction.io/install/

##### ADD A PAGE OR TWO OF INSTALL METHODS

####Step ii starting the event server
PredictionIO is not a monolithic humongous application. Rather, it is a collection of specialized servers and other applications.  One such specialized server is what PredictionIO calls the Event Server.  In our “leap before understanding what’s going on” approach that we’ve been using, let’s start that server and then we will figure out what it does.
To start the eventserver, type the following in a terminal window:

```
pio eventserver --ip 0.0.0.0 &
```

The Event Server is the PredictionIO component that imports and manages data. We will be looking at the Event Server in more detail.  For now let’s continue focusing on building our music recommendation system. 

> That’s it for the preliminary steps. We got the software installed and started the event server!

####step 1. generating an app ID and Access Key.
The Event Server might be storing data from a variety of sources and for a variety of applications. In this sense it is similar to a database server. A single database server can store numerous databases and each database can be tied to a unique application.  The Event Server is similar [change word] For example, the server might be storing information related to our music recommendation system, and also storing data related to an entirely different project. When we store data in the Event Server we want it to keep track of where that data came from and how it will be used. We want to say something like “Hey, here’s some data and remember it came from me, the music recommendation web app.” To make this connection we are going to generate a unique 64 byte Access Key by using the command pio app new:

```
vagrant~$ pio app new MusicApp
2015-... INFO  hbase.HBLEvents - The table predictionio_eventdata:events_1 doesnt exist yet. Creating now...
2015-... INFO  tools.Console$ - Initialized Event Store for this app ID: 1.
2015-... INFO  tools.Console$ - Created new app:
2015-... INFO  tools.Console$ - Name: MusicApp
2015-... INFO  tools.Console$ -         ID: 1
2015-... INFO  tools.Console$ - Access Key: PG9ydWoPHFbixNAuANUXWU5yTVCK4UV6VY6tA4zwh4SFRQIk8oacSvCQPSFD2eH6

```


Here we instruction pio (PredictionIO) to make a new app named “MusicApp” and pio generates and prints out the access key and an id (we will use the id shortly).

#### step 2. importing data
PredictionIO uses the term event to refer to one piece of data. For example, Jake giving a rating of 5 to Taylor Swift is an event. The type of the event is a rating--user Jake is giving an item, Taylor Swift, a rating of 5. The specific format of the event is

```
{
  "event" : "rate",
  "entityType" : "user"
  "entityId" : "Jake",
  "targetEntityType" : "item",
  "targetEntityId" : "Taylor Swift",
  "properties" : { "rating" : 5.0 }}

```

There are a number of ways to connect to the Event Server and transmit events. For Python, which we will use here, there is a module for predictionIO that provides an interface to the Event Server.  The first thing we need to do is install this module using the Python package manager, pip:

```
vagrant~$ pip install predictionio
```

If, when you try this you get the error: 

```
The program 'pip' is currently not installed. To run 'pip' please ask your administrator to install the package 'python-pip'
```

The program 'pip' is currently not installed. To run 'pip' please ask your administrator to install the package 'python-pip'you can install pip by executing:
```
vagrant~$ sudo apt-get install python-pip
```

and then rerunning pip install predictionio. 
Okay, back to our task of importing data to the Event Server using Python. First, we represent our music recommendation data shown in the table above in the text file shown below:  FIX XXX

>Jake,Taylor Swift,5
Jake,Brad Paisley, 5
Jake,Guardians of the Galaxy Awesome Mix Vol. 1,3
Jake,Ed Sheeran,3
Jake,Panda Bear,1
Clara,Guardians of the Galaxy Awesome Mix Vol. 1,5
Clara,Ed Sheeran,3
Clara,New Basement Tapes,4
Clara,Panda Bear, 4
Clara,Ariana Grande,5
Kelsey,Taylor Swift,5
Kelsey,Miranda Lambert,5
Kelsey,Brad Paisley, 5
Kelsey,Nicki Minaj,1
Kelsey,Guardians of the Galaxy Awesome Mix Vol. 1,3
Kelsey,Ed Sheeran,3
Angelina,Taylor Swift,2
Angelina,Miranda Lambert,2
Angelina,Brad Paisley, 1
Angelina,Baby Metal, 4
Angelina,Nicki Minaj,4
Angelina,Ariana Grande,5
Angelina,New Basement Tapes,3
Jorydyn,Brad Paisley,1
Jordyn,Baby Metal, 4
Jordyn,Guardians of the Galaxy Awesome Mix Vol. 1,5
Jordyn,Nicki Minaj,5
Jordyn,Panda Bear,1

> This data file as well as the Python code on the following page are  available at.. http://XXXXXXXX

Each line represents a single rating. For example, the first line represents the event of Jake giving Taylor Swift a rating of 5.

Next, we will run the following short Python script that will send this data to the event server.

```
import predictionio
DELIMITER = ","

def import_events(client, filename):
	count = 0
	with open(filename) as f:
		for line in f:
			data = line.rstrip('\r\n').split(DELIMITER)	
			client.create_event(
        		event="rate",
        		entity_type="user",
        		entity_id=data[0],
        		target_entity_type="item",
        		target_entity_id=data[1],
        		properties= { "rating" : float(data[2]) }
        	)   
			count += 1
  	
  	print "%s events are imported." % count

client = predictionio.EventClient(
    access_key='Kx1GhBg8b5PUVbg7Zicv4RWHqEeUNnUiz1EBIRqMfvjjSycOY2GT21AwE',
    url='http://localhost:7070',
    threads=5,
    qsize=500)
import_events(client, 'data/music.data')
```

(Replace that access key with your own.)
As you can see, this code opens the data file. It then iterates through each line of the data and imports that line of data into the Event Server. For example, processing the line:

```
Jake,Taylor Swift,5
```
Previously we saw that the Event Server can import data that is in the following format:
```
{
  "event" : "rate",
  "entityType" : "user"
  "entityId" : "Jake",
  "targetEntityType" : "item",
  "targetEntityId" : "Taylor Swift",
  "properties" : { "rating" : 5.0  }}

```
The Python code converts a line from the data file to this format before passing it to create_event which adds the data to the Event Server. 
Running this code will import the events (data) into the Event Server:

```
vagrant $ python data/import3.py 

28 events are imported.

```

![Alt text](http://guidetodatamining.com/markdownPics/programming3.png)

We can go to a browser window and enter the url:
http://localhost:7070/events.json?accessKey=<our access key>
So, with the access key we have been using above:
http://localhost:7070/events.json?accessKey=Kx1GhBg8b5PUVbg7Zicv4RWHqEeUNnU3iz1EBIRqMfvjjSycGUjv3XOY2GT21AwE
and our imported data will be displayed:
![Alt text](http://guidetodatamining.com/markdownPics/screenshot1.png)

(sorry for that tiny print). Anyway, it looks like we’ve been successful importing the data.

## Creating a recommendation engine
Now it is time to build a recommendation system. PredictionIO calls machine learning systems,  ‘engines’. An engine is a machine learning system configured to your specific application.

####step 3. base your engine on a template
We construct our engine in a series of steps. First, we are going to base our music recommender engine on a pre-existing template⎯in this case a recommendation template. We do that as follows:

```
vagrant:/vagrant$ pio template get PredictionIO/template-scala-parallel-recommendation musicRecommender
Please enter author's name: Ron Zacharski
Please enter the template's Scala package name (e.g. com.mycompany): org.zacharski
Please enter author's e-mail address: ron.zacharski@gmail.com
Would you like to be informed about new bug fixes and security updates of this template? (Y/n) ...

Engine template PredictionIO/template-scala-parallel-recommendation is now ready at musicRecommender
```

vagrant:/vagrant$ pio template get PredictionIO/template-scala-parallel-recommendation musicRecommender
Please enter author's name: Ron Zacharski
Please enter the template's Scala package name (e.g. com.mycompany): org.zacharski
Please enter author's e-mail address: ron.zacharski@gmail.com
Would you like to be informed about new bug fixes and security updates of this template? (Y/n) ...

Engine template PredictionIO/template-scala-parallel-recommendation is now ready at musicRecommenderThis step downloads  the most recent version of the recommendation template (template-scala-parallel-recommendation) and does some minimal configurations. (Later we will see how we can customize this engine further).  Now we have a musicRecommender engine that is based on the stock recommendation engine.

#### step 4. edit the engine.json config file
The step we just completed creates a directory musicRecommender. In our terminal window, let’s change to that directory and look at its contents:

```
vagrant:/vagrant$ cd MusicRecommender
vagrant:/vagrant/MusicRecommender$ ls
build.sbt  data  engine.json  manifest.json  pio.log  project  src  target
```
In step 2 we generated an app id and an access key. In that step’s example, the app id was 1. If we didn’t write that down and can’t remember, we can always find the app id and access key by asking PredictionIO to list the apps: 

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ pio app list
-        Name |   ID |                                    Access Key |
   MusicApp |    1 | Kx1GhBg8b5PUVbg7Zicv4RWHqEeUNnU3iz1EBIRqMfvjj |
     Movies |    2 | PG9ydWoPHFbixNAuANUXWU5yTVCK4UV6VY6tA4zwh4SFR |
      MyApp |    3 | B16gBfLR7tQq6dZhJQWAemB5Jmu11QFjCWyfPqiGrz9KW |

2015-03-01 16:26:23,028 INFO  tools.Console$ - Finished listing 3 app(s).

```

>[note] in this example I have elided some information (for example, I shortened the access keys) to make the example more legible while keeping a reasonable font size)

Great. So it is the case that the id for our MusicApp is 1. We need to make sure the engine we just created is tied to this app (in our case app id 1). 
To do this we need to edit the engine.json file in the musicRecommender directory so the app  ids match: 

```
{
  "id": "default",
  "description": "Default settings",
  "engineFactory": "org.zacharski.RecommendationEngine",
  "datasource": {
    "params" : {
      "appId": 1
    }
  },
```

####step 5. building the engine
Once you edit that file and save it, we can build the engine:

```
vagrant:/vagrant$ pio build

```

This takes about 5 minutes in a vagrant box on my Mac Desktop. Other than taking a long time and seeing some info print out it is not that rewarding of a step as far as seeing something get accomplished. 

 
> **Another note**
> If you get the error:
> 2015-03-06 19:44:52,324 ERROR tools.Console$ - Return code of previous step is 1. Aborting.
>   make sure you are in the musicRecommender directory when you execute pio build.

Now that it is accomplished we can finally train the recommender. 

#### step 6. training the engine

Remember our original table of data? 


| | Jake | Clara | Kelsey | Angelica | Jordyn |
|:-:|--:|--:|--:|--:|--:|
|Taylor Swift	| 5	| - 	| 5	| 2	| - |
|Miranda Lambert |	- |	-	| 5 |	2 | 	- |
| Brad Paisley	| 5	| - |	5	| 1	| 1 |
| Purity Ring |	- |	-	| -	 | 4	| 4 |
|Father John Misty |	3 |	5 |	3 | 	-	| 5 |
|Nicki Minaj |	-	| - | 	1	| 4 |	5 |
| Ed Sheeran	| 3 |	3	| 3 | 	- |	- |
| Ariana Grande |  	- |	- |	-	| 5 |	- |
| Flying Lotus |	-	| 4	| - | 3 | 	- |
| Thundercat |	1	| 4	| - | -	 |1 |

Training involves creating a system that will replace those unknown values (the hyphens) with good predictions of how that user would rate the artist. By default the recommendation engine uses a method called matrix factorization, which we will learn about in chapter 3. The basic idea is that the training starts by the engine building a recommendation system based on random values. Obviously, it will perform very poorly. Then we will run this recommendation system on our data and see how well it predicts our known values. For example, how well did it predict Jake would give a 5 to Taylor Swift. Let’s say the system predicted Jake would give Taylor Swift a 3. In that case we would adjust the parameters to increase the Jake-Taylor  Swift rating (and account for other mis-predictions). Now we have a second generation of our recommendation engine and we again evaluate it on our data and adjust the parameters. We will do this perhaps 1,000 times until our recommender is precise in predicting the known values. Now we can use this recommender to fill in those missing values.  Let’s go ahead and train our engine.

```
vagrant:/vagrant/MusicRecommender$ pio train
2015-03-03 21:51:33,577 INFO  tools.Console$ - Using existing engine manifest JSON at /vagrant/MusicRecommender/manifest.json
...
2015-03-03 21:52:02,754 INFO  workflow.CoreWorkflow$ - CoreWorkflow.run completed.
2015-03-03 21:52:02,757 INFO  workflow.CoreWorkflow$ - Your engine has been trained successfully.
```
Fantastic. It looks like we successfully trained a recommendation system. There is one final step to getting our music recommendation engine up and running.

####step 7. deploy
We are going to start our recommendation engine, which in essence is a server running on port 8000. The command we are going to use is pio deploy:

```
vagrant:/vagrant/MusicRecommender$ pio deploy --ip 0.0.0.0
2015-03-03 21:59:32,846 INFO  tools.RunServer$ - Submission command: /home/vagrant/PredictionIO/vendors/spark-1.2.0/bin/spark-submit --class io.
...
2015-03-03 21:59:46,064 INFO  workflow.MasterActor - Bind successful. Ready to serve.
```
That’s it, we build, trained, and  deployed our first PredictionIO recommendation engine.
What happens if we go to the url http://localhost:8000 in our browser?

![Alt text](http://guidetodatamining.com/markdownPics/screenshot2.png)

Okay. Everything looks like it is working.  Next step? Make some recommendations


####step 8. testing our system: making recommendations
Okay, I am going to show that original chart yet again.



| | Jake | Clara | Kelsey | Angelica | Jordyn |
|:-:|--:|--:|--:|--:|--:|
|Taylor Swift	| 5	| - 	| 5	| 2	| - |
|Miranda Lambert |	- |	-	| 5 |	2 | 	- |
| Brad Paisley	| 5	| - |	5	| 1	| 1 |
| Purity Ring |	- |	-	| -	 | 4	| 4 |
|Father John Misty |	3 |	5 |	3 | 	-	| 5 |
|Nicki Minaj |	-	| - | 	1	| 4 |	5 |
| Ed Sheeran	| 3 |	3	| 3 | 	- |	- |
| Ariana Grande |  	- |	- |	-	| 5 |	- |
| Flying Lotus |	-	| 4	| - | 3 | 	- |
| Thundercat |	1	| 4	| - | -	 |1 |

Before we let our new recommendation engine make predictions for Jake let’s pause and see what we humans might recommend. What do you think?
what do you think?
What artist would you recommend to Jake?  




  




Here’s my thinking. Jake looks similar to Kelsey. Both Jake and Kelsey gave a 5 to Taylor Swift and Brad Paisley and a 3 to Guardians of the Galaxy and Ed Sheeran. So I think Jake probably like what Kelsey likes. Kelsey gave Miranda Lambert a 5 so Jake would probably do so too. So I would recommend Miranda Lambert to Jake.
While we are at it let’s come up with a recommendation for Jordyn.  

Jordyn is most similar to Angelica and Angelica gave a 5 to Ariana Grande so that would be a good recommendation for Jordyn.
Those are the human recommendations. Let’s check out the machine.

On the left are Jake’s original ratings and again, we think Jake would give a 5 to Miranda Lambert so we recommend that to him. 
To ask our recommendation system let’s use curl, 
If you have never used curl before, it is simply a command line tool to transfer data to and from a server using url syntax.       
We are going to use curl to send a query to our recommendation engine (recall that is running at http://localhost:8000). The specific url that will handle our query is http://localhost:8000/queries.json   
Our query will be in a json format:  

```
  { "user": "Jake", "num": 4 } 
```


This query asks for the 4 highest rated items for Jake. Let’s put this together and ask the engine for some recommendations (this time, let’s ask for the 10 total ratings):

```
Lungta:~ raz$ curl -H "Content-Type: application/json" -d '{ "user": "Jake", "num": 10 }' http://localhost:8000/queries.json

{"itemScores":
[{"item":"Taylor Swift","score":4.997968289493851},    {"item":"Brad Paisley","score":4.992076869666511},
 {"item":"Miranda Lambert","score":4.882315027430614},
 {"item":"Guardians of the Galaxy Awesome Mix Vol. 1","score":  
  3.0009464062894144},
 {"item":"Ed Sheeran","score":2.988141238862262},
 {"item":"Ariana Grande","score":1.8154660104862221},
 {"item":"Baby Metal","score":1.4449050788629214},
 {"item":"New Basement Tapes","score":1.3243822061813184}, 
 {"item":"Nicki Minaj","score":1.0554909771692242},
 {"item":"Panda Bear","score":1.005113459149016}]
```

 Let’s compare these predicted ratings to Jake’s original ratings:

| - | Actual | Predicted |
|--:|--:|--:|
|Taylor Swift | 5 | 4.998 |
|Brad Paisley | ? | 4.882 |
| Purity Ring | ? | 1.445 |
| Father John Misty | 3 | 2.988 |
| Nicki Minaj | ? | 1.055 |
| Ed Sheeran | 3 | 2.988 |
| Ariana Grande | ? | 1.815 |
| Flying Lotus | ? | 1.324 |
| Thundercat | 1 | 1.005 |

Wow. That looks pretty good. Jake gave Taylor Swift a 5 and the recommender predicted a 4.998. Jake gave Brad Paisley a 5 and the recommender predicted a 4.992. But really, this isn’t that surprising. After all, we trained our recommendation system on this data. It would be more a surprise if the predicted ratings significantly differed from Jake’s true ratings. More interesting is what the recommender predicted for artists Jake didn’t rate--and perhaps never heard. It predicts that Jake should like Miranda Lambert and this matches our expectations-- We thought Jake would like Miranda Lambert. And that is pretty much all Jake will like from our short list of artists.

> ####You try
> Can you query our recommender to get the predicted values for Jordyn and fill in the following table?


