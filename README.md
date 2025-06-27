# ReelMetrics - How Early Reviews Effect Film Box Office Performance

## Authors
[Michael Neuhoff](https://github.com/neuhoffmj)    
[Michael Schiff](https://github.com/michaelleeschiff)  
[Danielle Wampler](https://github.com/wampler77)  

## Overview

In the film industry, it is generally assumed that early reviews correlate with good word-of-mouth for a movie. With good word of mouth, one would expect a movie to have smaller weekly drops in movie grosses leading to a higher overall gross at the box office. A way to quantify a movie's performance over time using a simple point estimate is the movie’s “Multiplier”. The Multiplier is calculated according to: 

```math
\text{Multiplier} = \frac{\text{Total Gross}}{\text{Opening}}
```
For this project, we carefully defined the multiplier based on a different number of theaters threshold for each movie. We then looked at review data from rotten tomatoes ([sourced from kaggle](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews)) to calculate average early reviews for each movie before the opening period concluded. We scraped data from ~18,000 movies on Box Office Mojo to get weeky gross tables for each using a custom scraping script. This data scraping and the cleaning and normalizing for the review data was extensive and represented a significant portion of the effort to get this project working.

## Structure of repository

- `AnalyzingReviewsAndBoxOffice.ipynb` in the root directory is a jupyter notebook containing our most complete set of findings after integrating review and box office data
- `Clean Data` contains our data scraping and cleaning scripts as well as final clean datasets in .csv and pickled .p formats
- `Exploratory Analysis` contains jupyter notebooks which examined our clean data. Of particular note, is our finalized methodology for calculating the multiplier in the `Exploratory Analysis/ExploringBoxOffice.ipynb`. We also include `ExploringFeatureRelationships.ipynb` which offers some insight into opportunities and challenges with creating a regression based predictive model based on box office data.

## Findings

- Across all movies, movie multipliers for movies with positive reviews and movie multipliers for movies with negative reviews were statistically different compared to movies with neutral reviews. As expected, movies with good early reviews had higher multipliers indicating higher grosses over time and movies with bad early reviews fared worse. 

- We also found noticeable differences in these trends when considering the genre of the movie. The difference in median multipliers was less for certain genres like romance and horror. In the industry these genres are often thought to have a "built-in" audience of fans and thus be less susceptible to the influence of reviewers. It also suggests that good early reviews are particularly important for the long-term success of sci-fi movies where the good-bad multiplier disparity is largest and to a high degree of statistical significance.  

