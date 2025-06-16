import csv
import pandas as pd

with open('rotten_tomatoes_movie_reviews.csv', newline='') as rawcsvfile:
    with open('rotten_tomatoes_movie_reviews_clean_binary.csv', 'w', newline = '') as cleanbcsvfile:
        with open('rotten_tomatoes_movie_reviews_clean_scale.csv', 'w', newline = '') as cleanscsvfile:
        
            csvread = csv.reader(rawcsvfile, delimiter=',')
            csvbwrite = csv.writer(cleanbcsvfile, delimiter=",")
            csvswrite = csv.writer(cleanscsvfile, delimiter=",")

            rawcount = 0
            cleanscount = 0
            cleanbcount = 0

            tracknulls =[]
            tracksnulls =[]
            trackbnulls =[]


            for row in csvread: 
                rawcount += 1
                if rawcount == 1: 
                    print(row)
                    for i in range(len(row)): 
                        tracknulls.append(0)
                        tracksnulls.append(0)
                        trackbnulls.append(0)

                if row[8] != '': #All reviews must have review text, audience needs to have review to read
                    if row[5] != '': #Data with reviewer original score
                        cleanscount += 1
                        csvswrite.writerow(row)

                        #track whats still missing in scale data
                        for i in range(len(tracksnulls)):
                            if row[i] == '': tracksnulls[i] += 1

                    if row[9] != '': #Data with binary p/n reviewer sentiment
                        cleanbcount += 1
                        csvbwrite.writerow(row)

                        #track whats still missing in scale data
                        for i in range(len(trackbnulls)):
                            if row[i] == '': trackbnulls[i] += 1

                if '' in row:
                    for i in range(len(tracknulls)):
                        if row[i] == '': tracknulls[i] += 1

            print ("Original row count:" + str(rawcount))
            print(tracknulls)
            print ("Cleaned row count (scale):" + str(cleanscount) + " (-" + str(rawcount-cleanscount) +")")
            print(tracksnulls)
            print ("Cleaned row count (binary):" + str(cleanbcount) + " (-" + str(rawcount-cleanbcount) +")")
            print(trackbnulls)

dfb = pd.read_csv('rotten_tomatoes_movie_reviews_clean_binary.csv', index_col=False)   
dfs = pd.read_csv('rotten_tomatoes_movie_reviews_clean_scale.csv', index_col=False)   

# initial df lengths
dfbol = dfb.shape[0]
dfsol = dfs.shape[0]

# remove duplicates
dfb.drop_duplicates()
dfs.drop_duplicates()

# final df lengths
dfbfl = dfb.shape[0]
dfsfl = dfs.shape[0]

# output unique dfs
dfb.to_csv('rotten_tomatoes_movie_reviews_clean_binary.csv', index=False)
dfs.to_csv('rotten_tomatoes_movie_reviews_clean_scale.csv', index=False)

print("scale data duplicates: " + str(dfsfl - dfsol))
print("binary data duplicates: " + str(dfbfl - dfbol))