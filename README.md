# ReelMetrics - How Early Reviews Effect Film Box Office Performance

## Authors
Michael Neuhoff
Michael Schiff
Danielle Wampler

## Overview

In the film industry, it is generally assumed that early reviews correlate with good word-of-mouth for a movie. With good word of mouth, one would expect a movie to have smaller weekly drops in movie grosses leading to a higher overall gross at the box office. A way to quantify a movie's performance over time using a simple point estimate is the movie’s “Multiplier”. The Multiplier is calculated according to: 

```math
\frac{\text{Total Gross}}{\text{Opening}} = \text{Multiplier}
```
And we carefully defined the multiplier for this project based on a different number of theaters threshold for each movie. We then looked at review data from rotten tomatoes ([sourced from kaggle](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews)) to calculate average early reviews for each movie before the opening period concluded. We scraped data from ~18,000 movies on Box Office Mojo to get weeky gross tables for each using a custom scraping script. This data scraping and the cleaning and normalizing for the review data was extensive and represented a significant portion of the effort to get this project working.

## Structure of repository

- `AnalyzingReviewsAndBoxOffice.ipynb` in the root directory is a jupyter notebook containing our most complete set of findings after integrating review and box office data
- `Clean Data` contains our data scraping and cleaning scripts as well as final clean datasets in .csv and pickled .p formats
- `Exploratory Analysis` contains jupyter notebooks which examined our clean data. Of particular not is our finalized methodology for calculating the multiplier in the `Exploratory Analysis/ExploringBoxOffice.ipynb`. We also include `ExploringFeatureRelationships.ipynb` which offers some insight into opportunities and challenges with creating a regression based predictive model based on box office data.

## Findings

- Across all movies, movie multipliers for movies with positive reviews and movie multipliers for movies with negative reviews were statistically different compared to movies with neutral reviews. As expected, movies with good early reviews had higher multipliers indicating higher grosses over time and movies with bad early reviews fared worse. 

- We also found noticeable differences in these trends when considering the genre of the movie. The difference in median multipliers was less for certain genres like romance and horror. In the industry these genres are often thought to have a "built-in" audience of fans and thus be less susceptible to the influence of reviewers. It also suggests that good early reviews are particularly important for the long-term success of sci-fi movies where the good-bad multiplier disparity is largest and to a high degree of statistical significance.  

We have identified on kaggle "Massive Rotten Tomatoes Movies & Reviews" which contains one dataset on movie info and another dataset on the critic information. The movie info dataset has the the following information on ~140k movies: movie id, title, audience score, tomatometer, rating, ratingcontent, release date, streaming release date, runtime, and genre. The critic review dataset has the follwoing information on ~1.4 million reviews: movie id, review id, creation date, critic name, top critic y/n, original critic score, review status (fresh/rotten), publication name, review text, and score sentiment (positive/negative). 
For movie gross over time, we have located the following website https://www.boxofficemojo.com/weekly/?ref_=bo_nb_wly_secondarytab which contains information on a week-to-week basis on individual movie gross time. We intend to scrape the weekly gross for movies on this website to produce a dataset with at least the approximate information: Movie name, week, year, rank, last week rank, gross, gross change %, theatres (#), theatre # change, average theatre gross, total gross, and distributor.
These would be our main three datasets which we would analyze in this project with the goal of connecting timestamped reviews to week-to-week success of the corresponding movies to discern to what extent this "multiplier" holds true and good early word of mouth from critics corresponds to maintained success as measured by a decreased change in movie gross from one week to the next. This datset does have information on audience scores, so we might have the data to push into more questions regarding connections between audience score, critic score, and gross should time permit. We have not located data on online search traffic at this time, but should the current goals move faster than expected, this might yet be another dataset we attempt to find or procure down the road.
One could imagine the "stakeholders" for this project could be the movie distributors and marketers. In this sense, the "stakeholders" for this project are the ones who could benefit from the knwoledge of if and how early critic reviews could help or hurt movie reception. In this way, the key performance indicators of this project could potentially be, roughly speaking:
  -> the strength of the relationship between positive overall critic reviews and prolonged success or negative overall critic reviews and movie fall off
  -> sensitivity of movie success to critic scores (or change in critic scores)
  These are of course initial thoughts and are subject to change and refinement upon more group discussion and as we progress in the project and get a stronger idea for the shape the project will be taking.
