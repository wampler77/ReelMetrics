import csv
import pandas as pd
from datetime import datetime
import math

dfb = pd.read_csv('rotten_tomatoes_movie_reviews_clean_binary.csv', index_col=False)   
#dfs = pd.read_csv('rotten_tomatoes_movie_reviews_clean_scale.csv', index_col=False)
dfr = pd.read_csv('rotten_tomatoes_movies_clean.csv', index_col=False)

ids = dfr['id']
titles = dfr['title']
release = dfr['releaseDateTheaters']

movie_ref = list(zip(ids, titles, release))

# data to cumulate and add
data = []

for movie in movie_ref:
    mid = movie[0]
    title = movie[1]
    release = movie[2]

    temp_weeks = []
    temp_sumbinary = []
    num_brevs = []
    temp_sumbinary_tc = []
    num_brevs_tc = []

    for index, row in dfb.iterrows():
        if row['id'] == mid:
            reld = datetime.strptime(release, "%Y-%m-%d")
            revd = datetime.strptime(row['creationDate'], "%Y-%m-%d")
            week = math.floor(((revd-reld).days)/7)
            week_ind = 0

            if week in temp_weeks:
                week_ind = temp_weeks.index(week)
            else:
                temp_weeks.append(week)
                temp_sumbinary.append(0)
                num_brevs.append(0)
                temp_sumbinary_tc.append(0)
                num_brevs_tc.append(0)
                week_ind = -1

            if row['scoreSentiment'] == "POSITIVE":
                temp_sumbinary[week_ind] += 1
                num_brevs[week_ind] += 1
                if row['isTopCritic'] == True: 
                    temp_sumbinary_tc[week_ind] += 1
                    num_brevs_tc[week_ind] += 1

            if row['scoreSentiment'] == "NEGATIVE":
                temp_sumbinary[week_ind] -= 1
                num_brevs[week_ind] += 1
                if row['isTopCritic'] == True: 
                    temp_sumbinary_tc[week_ind] -= 1
                    num_brevs_tc[week_ind] += 1

    avbinary = []
    avbinary_tc = []
    for i in range(len(temp_sumbinary)):
        avbinary.append(temp_sumbinary[i]/num_brevs[i])
        if num_brevs_tc[i] != 0:
            avbinary_tc.append(temp_sumbinary_tc[i]/num_brevs_tc[i])
        else:
            avbinary_tc.append(0)

    #add movie data
    for wi in range(len(temp_weeks)):
        print([mid, title, release, temp_weeks[wi], temp_sumbinary[wi], avbinary[wi], num_brevs[wi], temp_sumbinary_tc[wi], avbinary_tc[wi], num_brevs_tc[wi]])
        data.append([mid, title, release, temp_weeks[wi], temp_sumbinary[wi], avbinary[wi], num_brevs[wi], temp_sumbinary_tc[wi], avbinary_tc[wi], num_brevs_tc[wi]])

dfn = pd.DataFrame(data)

# output unique dfs
dfn.to_csv('rotten_tomatoes_movie_reviews_weekly.csv', index=False)

print(dfn.head(10))
            