import csv
import pandas as pd

with open('../rawdata/rotten_tomatoes_movies.csv', newline='') as rawcsvfile:
    with open('rotten_tomatoes_movies_clean.csv', 'w', newline = '') as cleancsvfile:
        
        csvread = csv.reader(rawcsvfile, delimiter=',')
        csvwrite = csv.writer(cleancsvfile, delimiter=",")

        rawcount = 0
        cleancount = 0

        tracknulls =[]
        trackcnulls =[]

        for row in csvread: 
            rawcount += 1
            if rawcount == 1: 
                print(row)
                for i in range(len(row)): 
                    tracknulls.append(0)
                    trackcnulls.append(0)

            if row[0] != '' and row[1] != '' and row[6]!= '': #All movies must have id, title and theater release date
                cleancount += 1
                csvwrite.writerow(row)

                #track whats still missing in scale data
                for i in range(len(trackcnulls)):
                    if row[i] == '': trackcnulls[i] += 1

                    
            if '' in row:
                for i in range(len(tracknulls)):
                    if row[i] == '': tracknulls[i] += 1

    print ("Original row count:" + str(rawcount))
    print(tracknulls)
    print ("Cleaned row count:" + str(cleancount) + " (-" + str(rawcount-cleancount) +")")
    print(trackcnulls)

dfc = pd.read_csv('rotten_tomatoes_movies_clean.csv', index_col=False)   

# initial df lengths
dfcol = dfc.shape[0]

# remove duplicates
dfc.drop_duplicates()

# final df lengths
dfcfl = dfc.shape[0]

# output unique dfs
dfc.to_csv('rotten_tomatoes_movies_clean.csv', index=False)

print("movie duplicates: " + str(dfcol - dfcfl))