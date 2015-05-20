
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
####a closer look at the recommendation engine 
## 2. recommender details
#### draft in progress

 In the last chapter we built our first recommendation system and its recommendations seemed to match what we expected. But how did it really come up with those recommendations? 
 
 Recall that when we built our recommendation system we based it on a template:
 
 
     ~$ pio template get PredictionIO/template-scala-parallel-recommendation musicRecommender
     Please enter author's name: Ron Zacharski
     Please enter the template's Scala package name (e.g. com.mycompany): org.zacharski
     Please enter author's e-mail address: ron.zacharski@gmail.com
     Would you like to be informed about new bug fixes and security updates of this template? (Y/n) ...
     
	Engine template PredictionIO/template-scala-parallel-recommendation is now ready at musicRecommender


This command downloads the recommender template, template-scala-parallel-recommendation-0.3.0, and places the files that make up this template in a directory called `musicRecommender`. In that directory we see a file titled `engine.json`, which we edited to add our appName, `MusicApp`:

	{
	  "id": "default",
	  "description": "Default settings",
	  "engineFactory": "org.zacharski.RecommendationEngine",
	  "datasource": {
	    "params" : {
      "appName": "MusicApp"
	    }
	  },
	  "algorithms": [
	    {
	      "name": "als",
	      "params": {
	        "rank": 10,
	        "numIterations": 20,
	        "lambda": 0.01,
	        "seed": 3
	      }
	    }
	    ]	
	}

One interesting part of this file is that we see that the recommender is using the ALS algorithm (alternating least squares) and we pass that algorithm several parameters such as rank and number of iterations. Let's check out how this ALS algorithm works.

The Basics
--

Let's say we work in a vinyl record and CD store downtown. A customer comes in and asks us for a recommendation. We ask the obvious question "What do you like?" and she responds with "I like Taylor Swift and Carrie Underwood." There are several ways we might come up with a recommendation for her. One is to reflect on regular customers to our store who bought albums from those artists and think what else they bought. Perhaps we notice that recently, people who bought Taylor Swift CDs also bought CDs by Miranda Lambert and we recommend Miranda Lambert to the new customer. This is a two step process. First, we determine previous customers who are most similar to the person standing in front of us and second, we look at what those previous customers bought and then use that information to make recommendations to our current customer. 

Another way we might come up with a recommendation is as follows. We know Taylor Swift and Carrie Underwood CDs share certain features. They both, obviously, have prominent female vocals. They both feature singer-songwriters They both have country influences and no PBR&B influences (the term PBR&B, aka hipster R&B and R neg B, is a portmanteau of PBR--Pabst Blue Ribbon, the hipster beer of choice--and R&B).  Then we think "Hey, Miranda Lambert CDs also have prominent female vocals and have country influences but no PBR&B influences, and we recommend Miranda Lambert to our new customer. With this recommendation method we extract a set of features from CDs this person likes and then think what other CDs share these features. 

Let's check this out a bit further. We will restrict ourselves to two features (country and PBR&B influences), five artists (Taylor Swift, Miranda Lambert,  Carrie Underwood, Jhené Aiko, and The Weeknd) and two customers (Jake and Ann).  As owners of the vinyl record store we have gone through and meticulously rated artists on these features. 

|Artist| Country| PBR&B|
|:-----------|:------:|:------:|
| Taylor Swift | 0.90 | 0.05|
|Miranda Lambert | 0.98| 0.00|
|Carrie Underwood|0.95| 0.03|
| Jhené Aiko | 0.01 | 0.99 |
| The Weeknd | 0.03 | 0.98 |

So Taylor Swift exudes a lot of country influences (0.90) but little PBR&B (0.05).

When customers come into our store we ask them on a scale of 0 to 5 how well they like country and how well they like PBR&B:

|Customer| Country| PBR&B|
|:-----------|:------:|:------:|
| Jake | 5 | 1|
|Ann | 0| 5|

Suppose Jake comes into the store,  has never heard of Miranda Lambert, and we are trying to predict how he might rate her. Jake rated country music a 5 and Miranda is 0.98 country so we multiply those numbers together.

$$5 \times 0.98 = 4.9$$

We do the same for the PBR&B numbers and add them together to get our estimate of Jake's rating of Miranda Lambert.

$$rating_{Jake,Miranda} =  5 \times 0.98 + 1 \times 0.05 = 4.9 + 0.05 = 4.95$$

>####Question
>What is Ann's ratings of Taylor Swift and Jhené Aiko?

$$rating_{a,ts} = 0 \times  0.9 + 5 \times .05 = 0.25$$

$$rating_{a,ja} = 0 \times 0.01  + 5 \times  0.99 = 4.95$$

####a slight change
Let's change this scenario a bit. Suppose we still rate our artists as above, but this time instead of asking customers about how well they like country and PBR&B we ask them how well they like various artists and we get something like the following (a question mark indicates that that customer has not rated that artist):

|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|5|?|5|2|2|
|Clara|2|?|?|4|5|
|Kelsey|5|5|5|2|?|
|Ann|2|3|?|5|5|
|Jessica|2|1|?|5|?|

Based on the table of the country and PBR&B influences of various artists and our customer artist rating table we would like to predict how well our customers like country and PBR&B:

|Customer| Country| PBR&B|
|:-----------|:------:|:------:|
| Jake | ? | ?|
| Clara | ? | ?|
| Kelsey | ? | ?|
|Ann | ?| ?|
| Jessica | ? | ?|

>####Take a moment
> Can you fill in the table above with just rough guesses? 

My feeling is that you can guess these values very accurately. For example, you probably gave Jake a 5 for country and a 2 for PBR&B and Jessica a 1.5 for country and a 5 for PBR&B. 

So now we have estimates for how well our customers like country and PBR&B.  Jessica comes into our store. She hasn't rated Carie Underwood or The Weeknd and we are trying to decide which of those two we should recommend to her.  Here are the tables we will need:



|Customer| Country| PBR&B|
|:-----------|:------:|:------:|
| Jake | 5 | 2|
| Clara | 2 | 4.5?|
| Kelsey | 5 | 2|
|Ann | 2.5| 5|
| Jessica | 1.5 | 5|



|Artist| Country| PBR&B|
|:-----------|:------:|:------:|
| Taylor Swift | 0.90 | 0.05|
|Miranda Lambert | 0.98| 0.00|
|Carrie Underwood|0.95| 0.03|
| Jhené Aiko | 0.01 | 0.99 |
| The Weeknd | 0.03 | 0.98 |

So, doing the math:


$$rating_{Jessica,CarrieUnderwood} = 1.5 \times  0.95 + 5 \times .03 = 1.57$$

$$rating_{Jessica,TheWeeknd} = 1.5 \times 0.03  + 5 \times  0.98 = 4.95$$

So we would recommend The Weeknd to Jessica.

I am going to call the table of ratings *R*:


|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|5|?|5|2|2|
|Clara|2|?|?|4|5|
|Kelsey|5|5|5|2|?|
|Ann|2|3|?|5|5|
|Jessica|2|1|?|5|?|

the table of how well users like various features *P*:


|Customer| Country| PBR&B|
|:-----------|:------:|:------:|
| Jake | 5 | 2|
| Clara | 2 | 4.5|
| Kelsey | 5 | 2|
|Ann | 2.5| 5|
| Jessica | 1.5 | 5|

and the table matching artists to various features *Q*:

|Artist| Country| PBR&B|
|:-----------|:------:|:------:|
| Taylor Swift | 0.90 | 0.05|
|Miranda Lambert | 0.98| 0.00|
|Carrie Underwood|0.95| 0.03|
| Jhené Aiko | 0.01 | 0.99 |
| The Weeknd | 0.03 | 0.98 |

We've seen that if we have *P* and *Q* we can figure out *R*.  And we have just seen that if we have *Q* and *R* we can figure out *P*. Can we figure out *Q*, the table indicating the country and PBR&B influences of the artists from *R* the table of customers rating artists and *P* the table of how well customers like country and PBR&B? 

>####Take a moment and decide
> Take a look at the above tables and see if that is true.

It is the case that if we know how customers rated artists (*R*) and how well customers like country and PBR&B music (*P*) we can figure out the country and PBR&B influences of the artists (*Q*). 

You may be wondering what this has to do with the topic we started this chapter with, namely the ALS algorithm, since in the previous chapter when we built our recommender we didn't specify any features.

### Matrix Factorization
For matrix factorization we don't tell the algorithm a preset list of features (female vocal, country, PBR&B, etc.). Instead we give the algorithm a chart (matrix) like the following:



|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|5|?|5|2|2|
|Clara|2|?|?|4|5|
|Kelsey|5|5|5|2|?|
|Ann|2|3|?|5|5|
|Jessica|2|1|?|5|?|


and ask the algorithm to extract a set of features from this data. To anthropomorphize this yet even more, it is like asking the algorithm, *Okay algorithm, given 2 features (or some number of features) call them feature 1 and feature 2, can you come up with the P and Q matrices?*  These extracted features are not going to be something like 'female vocals' or 'country influence'. In fact, we don't care what these features represent. Again, we are going to ask the algorithm to extract features that are hidden in that table above. In order to make this sound a bit fancier than 'hidden features' data scientists use the Latin word for 'lie hidden', *lateo*, and call these **latent features**.

The inputs to the matrix factorization algorithm are the data in the chart shown above and the number of latent features to use (for example, 2). Our eventual goal is to calculate  $\hat{R}$ a table of estimated ratings. That is, a table similar to the above but with all the numbers filled in:

|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood |Jhené Aiko| The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|4.92|**4.78**|4.94|1.79|2.17|
|Clara|2.16|**2.97**|**1.64**|4.30|4.62|
|Kelsey|4.98|4.91|4.96|2.12|**2.52**|
|Ann|2.04|2.99|**1.45**|4.79|5.13|
|Jessica|1.79|**2.80**|1.16|4.89|**5.22**|

The bolded numbers are those that were blank in the original chart but predicted by our algorithm. The unbolded numbers are predicted values that have an actual value in the original table.  From our original data we see that Jake gave a rating of 5 to both Taylor Swift and Carrie Underwood and we see that the algorithm's estimates for those are 4.92 and 4.94---pretty good!
To get these predicted values we use latent features as an intermediary. Let's say we have two features: *feature 1* and *feature 2*. And, to keep things simple, let's just look at how to get Jake's rating of Taylor Swift.  Jake's rating is based solely on these two features and for Jake, these features are not equal in importance but are weighed differently. For example, Jake might weigh these features:

|       -   | Feature 1 | Feature 2 |
|:-----|:----:|:----:|
| Jake |0.717 | 2.309 |


So feature 2 is much more influential in Jake's rating than feature 1 is.  

We are going to have these feature weights for all our users and, again, by convention we call the resulting matrix, *P*:



|       -   | Feature 1 | Feature 2 |
|:-----|:----:|:----:|
| Jake | 0.717 | 2.309 |
| Clara | 1.875 | 0.437 |
| Kelsey | 0.861 | 2.288 |
| Ann | 2.10 | 0.295 |
| Jessica | 2.14 | 0.145 |


The word 'matrix' just means a table of numbers, just like we have above.

The other thing we need is how these features are represented in Taylor Swift-- how much "Feature 1-iness IS Taylor Swift? So we need a table of weights for the artists and again by convention, we call this matrix *Q*:



 
 Artist | Feature 1 | Feature 2 |
|:-----|:----:|:----:|
| Taylor Swift | 0.705 | 1.913 |
| Miranda Lambert | 1.189 | 1.700 |
| Carrie Underwood | 0.407| 2.015 |
| Jhené Aiko | 2.276 | 0.072 |
| The Weeknd | 2.419 | 0.191 |


Now back to our task of predicting how Jake will rate Taylor Swift ...




If we want to know how Jake will rate Taylor Swift we take Jake's weights for these features


|       -   | Feature *x* | Feature *y* |
|:-----|:----:|:----:|
| Jake | 0.717 | 2.309 |

and Taylor Swift's:

 Artist   | Feature *x* | Feature *y* |
|:-----|:----:|:----:|
| Taylor Swift  | 0.705 | 1.913 |

Multiply together Jake's and Taylor Swift's values for each feature:


|       -   | Feature *x* | Feature *y* |
|:-----|:----:|:----:|
| Jake| 0.717 | 2.309 |
| Taylor Swift  | 0.705 | 1.913 |
| **Product** | 0.505| 4.417 |

Then add those products up to get the predicted rating, *r*

$$ r =0.505 + 4.417 = 4.92$$

#### Dot Product

This operation is called the dot product. A list of numbers, for example, Jake's weights for the features: [0.717, 2.309] is called a **vector**. A dot product is performed on two vectors of equal length and produces a single value. It is defined as follows:

Let A and B be two vectors of equal length. Then

$$A \cdot  B = \sum_{i=1}^nA_iB_i=A_1B_1+A_2B_2+A_1B_1+...A_nB_n$$

So, for example, if

$$A = [1, 3, 5, 7, 9]$$

and 

$$B = [2, 4, 6, 8, 10]$$

then the dot  product of A and B is

$$A \cdot B = 1 \times 2 + 3 \times 4 + 5 \times 6 + 7 \times 8 + 9 \times 10 =  190$$

 

So above we determined Jake's rating of Taylor Swift by getting the dot product of Jake, *J* and Taylor Swift, *S*:

$$J \cdot  S = 0.717 \times 0.705 +  2.309 \times 1.913 = 4.92$$

And, since I am giving things fancy names in this section,  I am going to call the Table from users to weights of the different features, Matrix P and the table from artists to weight Matrix Q. Once we have P and Q it is easy to make predictions. 

#### Multiplying matrices
Great. We now have an estimate of how Jake will rate Taylor Swift. Now we want to do this for all user, artist pairs to get $\hat{R}$  (the little hat over the *R* indicates it is our estimate of the ratings). The actual ratings are in the matrix *R* above. We get $\hat{R}$ by multiplying the *P* and *Q* matrices together.  Here's the thing about multipying matrices. To multiply matrices one matrix needs to have the same number of columns as the other has rows. If you look at *P* and *Q* above you can see that this is not the case. To make this work out mathematically, we need to flip one of the matrices on-end so that the rows become the columns. Let's do this for matrix Q. So *Q* originally is 



Artist  | Feature 1 | Feature 2 |
|:-----|:----:|:----:|
| Taylor Swift | 0.705 | 1.913 |
| Miranda Lambert | 1.189 | 1.700 |
| Carrie Underwood | 0.407| 2.015 |
| Jhené Aiko | 2.276 | 0.072 |
| The Weeknd | 2.419 | 0.191 |



and flipped:

|feature: | Taylor Swift | Miranda Lambert | Carrie Underwood | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|1|0.705|1.189|0.407|2.276|2.419|
|2|1.913|1.700|2.015|0.072|0.191|


This flipping of the table (or matrix) is called transposing the matrix.  If the original matrix is called *Q* the transpose of the matrix is indicated by $Q^T.$ 
So now when you see $Q^T$ you don't need to freak out. Just think, oh, I just flip the matrix so rows become columns.  Cool. And our estimate of the ratings equals:

$$\hat{R} = PQ^T$$

or in our case of customers and artists:

$$\hat{R} =\begin{bmatrix}
0.717 & 2.309 \\
1.875 & 0.437 \\
0.861 & 2.288 \\
2.100 & 0.295 \\
2.140 & 0.145
\end{bmatrix}  \times
 \begin{bmatrix}
0.705 & 1.189 & 0.407 & 2.276 & 2.419  \\
1.913 & 1.700 & 2.015 & 0.072 & 0.191
\end{bmatrix} $$
and when we do this multiplication we will get the filled in version of our estimated ratings table:


|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Nicki Minaj | Ariana Grande |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|-|-|-|-|-|
|Clara|-|-|-|-|-|
|Kelsey|-|-|-|-|-|
|Angelica|-|-|-|-|-|
|Jordyn|-|-|-|-|-|

Here is how we multiply matrices *P* and $Q^T$ together.  To get the value of the first row, first column of our result (in our case Jake's estimated rating of Taylor Swift) we take the dot product of the first row of *P* and the first column of $Q^T.$  

![Multiplying first row of *P* by first row of *Q*](http://guidetodatamining.com/markdownPics/firstRow1.png)


$$ = 0.717 \times 0.705 + 2.309 \times 1.913 = 4.92$$

|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Nicki Minaj | Ariana Grande |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|4.92|-|-|-|-|
|Clara|-|-|-|-|-|
|Kelsey|-|-|-|-|-|
|Angelica|-|-|-|-|-|
|Jordyn|-|-|-|-|-|

To get the estimated value for row one column two (Jake's rating of Miranda Lambert) we take the dot product of the first row of *P* and the second column of  $Q^T:$


![Multiplying first row of *P* by second row of *Q*](http://guidetodatamining.com/markdownPics/firstRow2.png)

$$ = 0.717 \times 1.189 + 2.309 \times 1.700 = 4.77$$



|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Nicki Minaj | Ariana Grande |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|4.78|4.77|-|-|-|
|Clara|-|-|-|-|-|
|Kelsey|-|-|-|-|-|
|Angelica|-|-|-|-|-|
|Jordyn|-|-|-|-|-|

and so on.

Once we have *P* and *Q* it is easy to generate estimated ratings. But how do we get these matrices?

###How do we get Matrices P and Q?
There are several common ways to derive these matrices. One method is called **stochastic gradient descent.** The basic idea is this. We are going to randomly select values for *P* and *Q*.  For example, we would randomly select initial values for Jake:

Jake = [0.03, 0.88]

and randomly select initial values for Taylor Swift:

Taylor = [ 0.73,  0.49]

So with those initial ratings we get a prediction of 
$$J \cdot  S = 0.03 \times 0.73 +  0.88 \times 0.49 = 0.45$$

which is a particularly bad guess considering Jake really gave Taylor Swift a '5'. So we adjust those values. We underestimated Jake's rating of Taylor Swift so we boost maybe something like:

Jake = [0.12, 0.83]

Taylor = [ 0.80,  0.47]

and now we get:

$$J \cdot  S = 0.12 \times 0.80 +  0.83 \times 0.47 = 0.49$$

That is better than before but still we underestimated so we adust and try again. And adjust and try again. We repeat this process thousands of times until our predicted values get close to the actual values. The general algorithm is

1. generate random values for the P and Q matrices
2. using these P and Q matrices estimate the ratings (for ex., Jake's rating of Taylor Swift).
3. compute the error between the actual rating and our estimated rating (for example, Jake actually gave Taylor Swift a '5' but using P and Q we estimated the rating to be 0.45. Our error was 4.55. 
4. using this error adjust P and Q to improve our estimate
5. If our total error rate is small enough or we have gone through a bunch of iterations (for ex., 4000) terminate the algorithm. Else go to step 2.

For how simple this algorithm is, it works surprisingly well.

The other method of estimated *P* and *Q* is called alternating least squares or ALS and this is the one our PredictionIO recommendation engine uses.

##Alternating Least Squares

Let's remind ourselves of the task. We are given matrix *R* and we would like to estimate *P* and *Q*. Recall that earlier in the chapter we determined that if we had 2 of the matrices we could determine the third. The example used in that section was that if we had the matrix of users rating different artists


|Customer | Taylor Swift | Miranda Lambert | Carrie Underwood | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|5|?|5|2|2|
|Clara|2|?|?|4|5|
|Kelsey|5|5|5|2|?|
|Ann|2|3|?|5|5|
|Jessica|2|1|?|5|?|


 and the matrix of how much country and PBR&B influences those artists exhibit 
 
 |Artist| Country| PBR&B|
|:-----------|:------:|:------:|
| Taylor Swift | 0.90 | 0.05|
|Miranda Lambert | 0.98| 0.00|
|Carrie Underwood|0.95| 0.03|
| Jhené Aiko | 0.01 | 0.99 |
| The Weeknd | 0.03 | 0.98 |

 
 we could determine how much each customer liked country and PBR&B. We also saw that if we had the matrix of users rating different artists and a matrix representing how much each customer liked country and PBR&B, then we could determine the country and PBR&B influences for each artist.  So as long as we had two of the matrices we could determine the third. Unfortunately we only have one of the matrices, not two. It seems we are stuck. But there is a way to bootstrap our way of of this problem. We simply randomly guess the values of one of the other two matrices. Suppose we guess at the values of *Q*. Now we have two matrices, *R* and *Q* and we can determine *P*. Now we have all three matrices but for *Q* we just took a random guess, so it is a bit dodgy. But that is okay because now we have *P*, and with *P* and *R* we can determine a better guess for *Q*. So we do that.

Now *P* is a bit dodgy as well since it was based on our original wild guess for *Q*, but now that we have a better value for *Q* we can use that to recompute *P*.  So the algorithm is this.

1. compute random values for *Q*
2. use that and *R* to compute *P* 
3. use that and *R* to compute *Q*
4. while we haven't reached the max number of iterations go to 2.

The word *alternating* in *alternating least squares* is based on us alternating our computations of *P* and *Q*. Now you may be wondering what the *least squares* bit means. We are given the matrix *R* and initially we compute random values for *Q*. Then, using *R* and *Q* we are going to compute the best possible *P*. But what do we mean by *best possible*? Let's say *R* the ratings customers gave artists is:


|Customer | Taylor Swift | Miranda Lambert | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|5|?|2|2|
|Ann|2|?|5|?|


and using the *Q* and *R* matrices we get $\hat{R}$ our estimate of *R*.


|Customer | Taylor Swift | Miranda Lambert | Jhené Aiko | The Weeknd |
|:-----------|:------:|:------:|:---------:|:------:|:--------:|
|Jake|2.5|?|1.0|3.5|
|Ann|5.0|?|3.5|?|


So how good of a guess is it? Well, let's see. Jake really gave Taylor Swift a 5 and our algorithm predicted a 2.5. That is 2.5 different. And Jake gave Jhené Aiko a 2 and our algorithm predicted a 1. That is 1 different. It sounds like a good idea might be to add up all these differences. The one twist we do is square the difference. So for each artist we subtract what our algorithm predicted from Jake's actual rating and square that. Then we sum those up:

$$SquaredError = (5-2.5)^2 + (2 - 1)^2 + (2 - 3.5)^2 + (2 - 5)^2 + (5 - 3.5)^2$$$ = 6.25 + 1 + 2.25 + 9 + 2.25 = 20.75

The smaller this number is, the closer our estimate is to Jake's real ratings.  So to start we have the real ratings $R$ and our guess for *Q*  and using those we are going to select a *P* which has results in the smallest squared error. Once we have this *P* we hold it constant and use it and $R$ to determine the *Q* that results in the least squared error and so on. So the least squares bit of *Alternating Least Squares* means using this measure to compute how close our estimate is to the real ratings.


## back to PredictionIO
Recall that when we looked at the engine.json file we saw several parameters being sent to the ALS algorithm:


	{
	  "id": "default",
	  "description": "Default settings",
	  "engineFactory": "org.zacharski.RecommendationEngine",
	  "datasource": {
	    "params" : {
      "appName": "MusicApp"
	    }
	  },
	  "algorithms": [
	    {
	      "name": "als",
	      "params": {
	        "rank": 10,
	        "numIterations": 20,
	        "lambda": 0.01,
	        "seed": 3
	      }
	    }
	    ]	
	}

#####rank
The rank parameter specifies how many latent features to have. As you can see when we built our recommender in chapter one we used 10 latent features.  The more latent features you have the better the accuracy of the recommender. For example, one seminal paper in this area [Large-scale Parallel Collaborative Filtering for the Netflix Prize](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=B446F454E5DD7BDDA0FD717CF8A5F1CC?doi=10.1.1.173.2797&rep=rep1&type=pdf) by Zhou et al. used 1000 features. However, the more latent features you use the more memory your recommender will take. In most cases a value between 10 and 500 is reasonable.
#####numIterations
As you can guess, this parameter refers to the number of iterations (repeating steps 2 and 3 above) the algorithm executes. As you might think, the more iterations, the better the results, but surprisingly, the algorithm needs very few iterations to produce good values for the *P* and *Q* matrices. Generally, a value between 10 and 20 will be sufficient.
#####lambda
In many machine learning algorithms, we train the algorithm on some set of data (called the training set) and once it is trained we use it on new data. There is a danger that the algorithm is so highly tuned to the training data that it performs poorly on the new data. This is called **overfitting**.   In the ALS algorithm, one potential cause of overfitting is having some latent features having extreme values. This lambda is roughly how much we are weighing these extreme values. The greater the lambda the more the algorithm dislikes solutions that contain extreme values.

#####seed
Recall the the first step of the algorithm is to generate random values for one of the matrices. Generally, each time we run the algorithm we get different initial values and because these initial values are different, the final results can vary as well. Often when we are testing, we want the algorithm to be deterministic and produce the exact same results each time we run it. To do so, we pass in a value for this seed parameter. In the example above, we passed the value 3 as a seed.

## Another dataset.
Before moving on, let's try building a recommender with a moderate sized dataset. The [ MovieLens Latest dataset](http://files.grouplens.org/datasets/movielens/ml-latest-README.html) contains slightly over 20 million ratings of about 27,000 movies by 229,000 users.  You already know all the steps to build a recommender. Can you do so with this data? The `ratings.csv` file contains lines like
$$1,122,5,838985046$$

which means that person 1 gave movie 122 a rating of a 5 at Unix timestamp 838985046 (Friday, August 2, 1996 at 11:24GMT).  The file movies.csv matches those movie IDs with actual movie titles (movie 122 in this case is Boomerang). We could import our data as before using a similar python script but there is a faster way to load large datasets.  We will first use the following Python script to convert the movie data into a json file:

```
 
import predictionio
exporter = predictionio.FileExporter(file_name="my_events.json")

def readMovieInfo(filename):
	movies = {}
	with open(filename) as f:
		for line in f:
			entry = line.split(",")
			movies[entry[0]] = entry[1]
	return movies

def import_events():
	movieInfo = readMovieInfo('ml-latest/movies.csv')
	count = -1
	with open('ml-latest/ratings.csv') as f:
		for line in f:
			if count >= 0:
				data = line.rstrip('\r\n').split(',')	
				#print data[2]
				exporter.create_event(
	        		event="rate",
	        		entity_type="user",
	        		entity_id=data[0],
	        		target_entity_type="item",
	        		target_entity_id=movieInfo[data[1]],

	        		properties= { "rating" : float(data[2]) }
	        		)   
			count += 1
			if count % 1000 == 0:
				print count
  	
  	print "%s events are imported." % count
  	exporter.close()

import_events()

```

The contents of the output json file look like:

```

{"eventTime": "2015-05-11T02:08:42.917+0000", "entityType": "user", "targetEntityType": "item", "event": "rate", "entityId": "1", "targetEntityId": "Interview with the Vampire: The Vampire Chronicles (1994)", "properties": {"rating": 3.0}}
{"eventTime": "2015-05-11T02:08:42.918+0000", "entityType": "user", "targetEntityType": "item", "event": "rate", "entityId": "1", "targetEntityId": "Jaws (1975)", "properties": {"rating": 3.0}}
{"eventTime": "2015-05-11T02:08:42.918+0000", "entityType": "user", "targetEntityType": "item", "event": "rate", "entityId": "1", "targetEntityId": "Scream (1996)", "properties": {"rating": 5.0}}
{"eventTime": "2015-05-11T02:08:42.918+0000", "entityType": "user", "targetEntityType": "item", "event": "rate", "entityId": "1", "targetEntityId": "Scream 2 (1997)", "properties": {"rating": 5.0}}

```

Now we can load the data into PredictionIO with the command

     pio import --appid 1 --input my_events.json

(or whatever the appid is in your case). On my, not particularly fast, machine it took slightly under 15 minutes.

As before we create  a recommendation Engine:

1. execute  `pio template get PredictionIO/template-scala-parallel-recommendation movieRecommender`
2.  edit the `engine.json` file to add the app name
3.  build the system by executing `pio build`

Before we train our system we will do one additional thing.


####Increasing the memory allocated to training
By default the amount of memory allocated for training is 512MB. Let's bump that up a bit. For me I am going to allocated 24GB, but use a number that is right for your system.

1. Within the PredictionIO directory there is the directory vendors/spark-1.3.0/conf. Within that folder make a copy of the spark-defaults.conf.template and call it spark-defaults.conf.
2. Edit the spark-defaults.conf file by uncommenting the `spark.driver.memory` line and changing the value from 5 to 24.
3. Adding the line `spark.executor.memory 24g`
4. save the file.

The resulting file should look like

```
# Example:
# spark.master                     spark://master:7077
# spark.eventLog.enabled           true
# spark.eventLog.dir               hdfs://namenode:8021/directory
# spark.serializer                 org.apache.spark.serializer.KryoSerializer
spark.driver.memory              24g
# spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three"
spark.executor.memory   24g

```

Let's go ahead and train our system. 

```
pio train
```

Depending on your machine training can take a long time. On my machine it took a bit under 15 minutes.

### How good is the recommender?
So we are sitting at a bar with our friends, all of whom also built recommenders for the Movie Lens data and we get to arguing about whose recommender is better. Is there an objective measure we could use to settle the argument?  A bit ago we talked about using a distance measure—if Jake's real rating of Taylor Swift was a 5 and our recommender predicted a 4.5 and Mary's recommender predicted a 4.75—Mary's recommendation is better since it is closer to the real rating.  But maybe Jake's rating of Taylor Swift  was a fluke and our recommender would do better with some other rating—say Clara's rating of Jhené Aiko. So we will test on a set of data where we know the ratings. Plus, we will test on data that hasn't been seen by the recommender.  And we will compute the average distance between our estimate and the real value. This is called root-mean-square-deviation and the formula is as follows:


$$
RMSD = \sqrt{\frac{\sum_{i=1}^{n}(r_i - \hat{r}_i)^2}{n}}
$$

*n* is the number of ratings in our test data. $r_i$ refers to the $i^{th}$ rating, for example, Jake rating Taylor Swift. $\hat{r}_i$ refers to our estimate of *r*. *RMSD* represents how far our recommender's estimates were off on average. So, an *RMSD* of 0.5 means that on average if the actual rating was a 4 our recommender might predict a 3.5 or 4.5.

####The effect of the number of latent features
A bit ago when we were looking at the engine.json file:



	{
	  "id": "default",
	  "description": "Default settings",
	  "engineFactory": "org.zacharski.RecommendationEngine",
	  "datasource": {
	    "params" : {
      "appName": "MusicApp"
	    }
	  },
	  "algorithms": [
	    {
	      "name": "als",
	      "params": {
	        "rank": 10,
	        "numIterations": 20,
	        "lambda": 0.01,
	        "seed": 3
	      }
	    }
	    ]	
	}


Here, rank refers to the number of latent features. I mentioned that the more latent features the more accurate the recommender. Let's see if this is the case with a small experiment.  Before I loaded the movielens data I removed 10 ratings. Thus, when the recommender was trained, it did not see these ratings.  My plan was to train a recommender that uses 2 features, 10, 50, and 100 and see which is better using *RMSE*. Here is the raw data of the results:

User | Movie | Actual | 2  | 10 | 50 | 100 | 
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
|2| Minority Report | 4 | 3.504 | 3.705 | 3.638 | 3,148|
|10| Star Wars IV | 5| 3.760 | 3.858 | 4.650 | 5.061 |
|33|KungFu Panda| 4 | 4.272 | 4.160|4.042|4.363|
|58|Gravity| 2.5|3.597|3.293| 3.265 | 3.043 |
|89|Interstellar|5| 5.121|4.867|4.876|5.020|
|101|Harry Potter -Chamber| 4| 4.079| 4.280|3.802|4.145|
|125|Mulholland Drive| 3 | 2.622|2.410|2.962|1.877|
|156|Frozen|5|3.281|3.703|3.618|4.645|
|211|Edge of Tomorrow|4|3.476|3.044|3.598|3.819|
|872|Eternal Sunshine|4|4.247|4.393|3.623|3.718|

And here is the resulting *RMSD:*

|latent features | 2 | 10 | 50 | 100 |
|:-----:|:-----:|:-----:|:-----:|:-----:|
|*RMSD*|0.80755| 0.7239|0.5576| 0.5174|

So our tiny experiment supports the previous substantial evidence that the more latent features the better the accuracy. Keep in mind that our experiment with only 10 test cases is tiny. It may offer support in a bar discussion, or may be a good late-night test to make sure we are not doing something screwy, but as we will see later, there are better ways to evaluate algorithm performance. 


