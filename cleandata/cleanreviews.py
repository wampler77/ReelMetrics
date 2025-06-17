import csv
import pandas as pd
from fractions import Fraction

with open('../rawdata/rotten_tomatoes_movie_reviews.csv', newline='') as rawcsvfile:
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

            print ("Original row count: " + str(rawcount))
            print(tracknulls)
            print ("Cleaned row count (scale): " + str(cleanscount) + " (-" + str(rawcount-cleanscount) +")")
            print(tracksnulls)
            print ("Cleaned row count (binary): " + str(cleanbcount) + " (-" + str(rawcount-cleanbcount) +")")
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
#dfs.to_csv('rotten_tomatoes_movie_reviews_clean_scale.csv', index=False) # commented bc further processing below

print("scale data duplicates: " + str(dfsfl - dfsol))
print("binary data duplicates: " + str(dfbfl - dfbol))

# normalize scaled reviews (originalScore)

grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F+', 'F', 'F-']
grade_conv = [1.0, 1.0, 0.925, 0.825, 0.75, 0.675, 0.575, 0.5, 0.425, 0.325, 0.25, 0.175, 0.075, 0, 0]

tonorm = []
tonorm_i = []
nonsenserevs = []
nonsenserevs_i = []

for i, row in dfs.iterrows():

    oS = dfs.at[i, 'originalScore']
    if oS[0] == "'" and oS[-1] == "'": oS = oS.replace("'", "")
    if oS[-1] == " ": oS = oS[:-1]
    if oS[0] == " ": oS = oS[1:]
    if "`" in oS: oS = oS.replace("`", "")
    if 'm inus' in oS: oS = oS.replace('m inus', 'minus')
    if 'min us' in oS: oS = oS.replace('min us', 'minus')
    if 'our of' in oS: oS = oS.replace('our', 'out')
    if 'outta' in oS: oS = oS.replace('outta', '/')
    if '\\' in oS: oS = oS.replace('\\', '/')
    if ':' in oS: oS = oS.replace(':', '/')


    if '/' in oS and (oS[0].isdigit() or oS[-1].isdigit()) and '*' not in oS: # Normalize fractions (oS[-1].isdigit() checking that there is a number at start and not a mixed letter grade i.e. B+/A-)
        tempoS = ''.join(ch for ch in oS if ch.isdigit() or ch == '/' or ch =='.') #some reviews had '' around the score, need to remove
        tempoS = tempoS.split("/")
        if tempoS[0].count('.') > 1 or tempoS[1].count('.') > 1: 
            nonsenserevs.append(oS) #this is a nonsense review with too many decimal points\
            nonsenserevs_i.append(i)
        elif float(tempoS[0]) == 0: oS = 0
        elif tempoS[1] == '': 
            nonsenserevs.append(oS) #this is a nonsense review to not specify what the review is out of
            nonsenserevs_i.append(i)
        elif float(tempoS[0]) > 0 and float(tempoS[1]) == 0: 
            nonsenserevs.append(oS) #this is a nonsense review to give something nonzero out of 0
            nonsenserevs_i.append(i)
        else: oS = float(tempoS[0])/float(tempoS[1])

        dfs.at[i, 'originalScore'] = oS

    elif oS in grades:
        oS = grade_conv[grades.index(oS)]
        dfs.at[i, 'originalScore'] = oS

    elif '4..+4' in oS: #almost all ratings given on scal -4..+4, except one typo 4..+4 but so unique a format that this should catch all and no extraneous data
        tempoS = oS.split(" ")
        if tempoS[0].lower() == 'high' or tempoS[0].lower() == 'low': tempoS = tempoS[1:]
        oS = (float(tempoS[0]) + 4.0) / 8.0
        dfs.at[i, 'originalScore'] = oS
    
    elif '*' in oS: # * denote stars
        fullstars = float(oS.count('*'))
        remoS = oS.replace('*', '')
        if '/' in remoS:
            remoS = remoS.split('/')
            oS = (float(float(remoS[0])/float(remoS[1])) + float(fullstars)) / 5.0
            dfs.at[i, 'originalScore'] = oS
        elif remoS == "":
            oS = fullstars
            dfs.at[i, 'originalScore'] = oS
        else:
            tonorm.append(oS)
            tonorm_i.append(i)

    elif '%' in oS and oS.replace('%', '').isdigit(): # giving a percent
        oS = float(oS.replace('%', ''))/100.0
        dfs.at[i, 'originalScore'] = oS

    elif oS[0].isalpha():
        tempoS = oS
        if 'minus' in tempoS:
            tempoS = tempoS.replace('-','')
            tempoS = tempoS.replace('minus','-')
            tempoS = tempoS.replace(' ', '')
        if 'plus' in tempoS: 
            tempoS = tempoS.replace('-','')
            tempoS = tempoS.replace('plus','+')
            tempoS = tempoS.replace(' ', '')

        if '+' in tempoS and ' ' in tempoS:
            tempoS = tempoS.replace(' ', '')
        if '-' in tempoS and ' ' in tempoS:
            tempoS = tempoS.replace(' ', '')
        if '-' in tempoS and '+' in tempoS: # if both + and - denoted, then take normal letter grade which is in between
            tempoS = tempoS.replace('-','')
            tempoS = tempoS.replace('+','')
            tempoS = tempoS.replace(' ', '')
        if '?' in tempoS: #if +/- unsure, denoted by ?, leave at normal letter grade. If not actual letter grade or stars, then should still be caught by tonorm array
            tempoS = tempoS.replace('?', '')
            tempoS = tempoS.replace(' ', '')
        if '=' in tempoS: #if reg letter grade, denoted by =, leave at normal letter grade. If not actual letter grade or stars, then should still be caught by tonorm array
            tempoS = tempoS.replace('=', '')
            tempoS = tempoS.replace(' ', '')

        if tempoS == 'A+++': tempoS = 'A+'
        if tempoS == 'F---': tempoS = 'F-'
        if tempoS == 'B--': tempoS = 'B-'
        if tempoS == 'C++': tempoS = 'C+'
        if tempoS == 'C--': tempoS = 'C-'
        if tempoS == 'A--': tempoS = 'A-'

        if tempoS.replace('_','').upper() in grades: #some reviews gave lower case grades
            oS = grade_conv[grades.index(tempoS.replace('_','').upper())]
            dfs.at[i, 'originalScore'] = oS

        elif "/" in tempoS and len(tempoS.split('/')) == 2:
            gradessplit = tempoS.split('/')
            if gradessplit[0].replace('_','').upper() in grades and gradessplit[1].replace('_','').upper() in grades:
                oS = (grade_conv[grades.index(gradessplit[0].replace('_','').upper())] + grade_conv[grades.index(gradessplit[1].replace('_','').upper())]) / 2.0
                dfs.at[i, 'originalScore'] = oS
            else:
                tonorm.append(oS)
                tonorm_i.append(i)

        elif 'star' in tempoS.lower():
            tempoS = tempoS.split(' ')
            score = tempoS[0].lower()
            scores = ['zero', 'one', 'two', 'three', 'four', 'five']
            score_conv = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

            if score in scores:
                oS = score_conv[scores.index(score)]
                dfs.at[i, 'originalScore'] = oS
            else:
                tonorm.append(oS)
                tonorm_i.append(i)
        
        # unclear word choices
        elif 'recommend' in oS.lower(): 
            nonsenserevs.append(oS) # Recommended or Not recommended is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'recomend' in oS.lower(): 
            nonsenserevs.append(oS) # same as above but accounting for typos
            nonsenserevs_i.append(i)
        elif 'short' in oS.lower(): 
            nonsenserevs.append(oS) # short is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'matinee' in oS.lower(): 
            nonsenserevs.append(oS) # matinee is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'rental' in oS.lower(): 
            nonsenserevs.append(oS) # rental is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'read a book' in oS.lower(): 
            nonsenserevs.append(oS) # read a book is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'price' in oS.lower(): 
            nonsenserevs.append(oS) # half price, etc. is a nonsense original review and is an unclear choice of unit
            nonsenserevs_i.append(i)
        elif 'watch' in oS.lower(): 
            nonsenserevs.append(oS) # big screen watch, etc. is a nonsense original review and is an unclear choice of unit
            nonsenserevs_i.append(i)
        elif 'catch' in oS.lower(): 
            nonsenserevs.append(oS) # catch it on cable, etc. is a nonsense original review and is an unclear choice of unit
            nonsenserevs_i.append(i)
        elif 'capsule' in oS.lower(): 
            nonsenserevs.append(oS) # capsule is a nonsense original review and adds nothing additional to sentiment
            nonsenserevs_i.append(i)
        elif 'non-numerical' in oS.lower(): 
            nonsenserevs.append(oS) # nonsense original review and is an unclear choice of scale
            nonsenserevs_i.append(i)
        elif 'bomb' in oS.lower(): 
            nonsenserevs.append(oS) # nonsense original review and is an unclear choice of scale
            nonsenserevs_i.append(i)
        elif 'g.o.a.t' in oS.lower(): 
            nonsenserevs.append(oS) # nonsense original review and is an unclear choice of scale
            nonsenserevs_i.append(i)
        elif 'goat' in oS.lower(): 
            nonsenserevs.append(oS) # nonsense original review and is an unclear choice of scale
            nonsenserevs_i.append(i)
        elif 'awful' in oS.lower(): 
            nonsenserevs.append(oS) # nonsense original review and is an unclear choice of scale
            nonsenserevs_i.append(i)
        else:   
            tonorm.append(oS)
            tonorm_i.append(i)

    elif (oS[0].isdigit() or (oS[0] == '.' and oS[1].isdigit())) and 'star' in oS.lower():
        tempoS = oS.split(' ')
        if len(tempoS) == 2 and (tempoS[1].lower() == 'stars' or tempoS[1].lower() == 'star'):
            if '-' in tempoS[0]: 
                nonsenserevs.append(oS) # this is a nonsense review, what does 1-2 (etc) stars mean
                nonsenserevs_i.append(i)
            elif '/' in tempoS[0]:
                fracscore = tempoS[0].split("/")
                oS = float(fracscore[0])/float(fracscore[1])
                dfs.at[i, 'originalScore'] = oS
            elif '.' in tempoS[0]:
                oS = float(tempoS[0])/5.0
                dfs.at[i, 'originalScore'] = oS
            else:
                oS = float(tempoS[0]) / 5.0
                dfs.at[i, 'originalScore'] = oS
        
        elif len(tempoS) == 3 and tempoS[2].lower() == 'stars':
            if len(tempoS[0]) == 1 and tempoS[0].isdigit() and  '/' in tempoS[1]:
                fracscore = tempoS[1].split("/")
                addfracscore = float(fracscore[0])/float(fracscore[1])
                oS = (float(tempoS[0]) + addfracscore) / 5.0
                dfs.at[i, 'originalScore'] = oS
            else:
                tonorm.append(oS)
                tonorm_i.append(i)

        elif 'out' in tempoS and 'of' in tempoS and len(tempoS) > 4:
            if tempoS[-1].lower() == 'stars' and tempoS[0][0].isdigit() and tempoS[3].isdigit() and len(tempoS) == 5:
                oS = float(tempoS[0]) / float(tempoS[3])
                dfs.at[i, 'originalScore'] = oS
            elif tempoS[-1].lower() == 'stars' and len(tempoS[0]) == 1 and tempoS[0].isdigit() and  '/' in tempoS[1] and tempoS[4].isdigit() and len(tempoS) == 6:
                fracscore = tempoS[1].split("/")
                addfracscore = float(fracscore[0])/float(fracscore[1])
                oS = (float(tempoS[0]) + addfracscore) / float(tempoS[4])
                dfs.at[i, 'originalScore'] = oS
            elif tempoS[1].lower() == 'stars' and tempoS[0][0].isdigit() and tempoS[-1].isdigit() and len(tempoS) == 5:
                oS = float(tempoS[0]) / float(tempoS[-1])
                dfs.at[i, 'originalScore'] = oS
            else: 
                tonorm.append(oS)
                tonorm_i.append(i)

        else:
            tonorm.append(oS)
            tonorm_i.append(i)

    elif oS[0].isdigit() and ('out' in oS or 'of' in oS):
        if '3of' in oS: oS = oS.replace('3of', '3 of') # fix singular typo
        tempoS = oS.split(' ')

        tempoS = [toS for toS in tempoS if toS.strip()] # remove null and empty elements

        if len(tempoS) == 3 and tempoS[0][0].isdigit() and tempoS[2][0].isdigit():
            oS = float(tempoS[0])/float(tempoS[2])
            dfs.at[i, 'originalScore'] = oS
        elif len(tempoS) == 4 and tempoS[0][0].isdigit() and tempoS[3][0].isdigit() and 'out' in oS and 'of' in oS:
            oS = float(tempoS[0])/float(tempoS[3])
            dfs.at[i, 'originalScore'] = oS
        elif 'ripples' in oS.lower(): 
            nonsenserevs.append(oS)   # num ripples is a nonsense original review and is not a discernable unit
            nonsenserevs_i.append(i)
        elif 'air tanks' in oS.lower(): 
            nonsenserevs.append(oS)   # num air tanks is a nonsense original review and is not a discernable unit
            nonsenserevs_i.append(i)
        elif 'pink ponies' in oS.lower(): 
            nonsenserevs.append(oS)   # num pink ponies is a nonsense original review and is not a discernable unit
            nonsenserevs_i.append(i)
        else: 
            tonorm.append(oS)
            tonorm_i.append(i)

    elif oS.replace('.', '').isdigit() or oS.replace('.', '') == '': 
        nonsenserevs.append(oS) # nonsense review made up of just numbers and decimals
        nonsenserevs_i.append(i)
    elif oS.replace(',', '').isdigit() or oS.replace(',', '') == '': 
        nonsenserevs.append(oS) # nonsense review made up of just numbers and commas
        nonsenserevs_i.append(i)
    elif oS.replace('-', '').isdigit() or oS.replace('-', '') == '': 
        nonsenserevs.append(oS) # nonsense review made up of just numbers and dashes
        nonsenserevs_i.append(i)
    elif oS[-1] == '/': 
        nonsenserevs.append(oS)  # nonsense review with no given scale
        nonsenserevs_i.append(i)
    elif 'ripples' in oS.lower(): 
        nonsenserevs.append(oS)  # num ripples is a nonsense original review and is not a discernable unit
        nonsenserevs_i.append(i)
    else:
        tonorm.append(oS)
        tonorm_i.append(i)

print("Remaining number of reviews to normalize: " + str(len(tonorm)))
print("Remaining reviews to normalize:")
print(tonorm)
print("Initial number of nonsense reviews: " + str(len(nonsenserevs)))

# If checked and none are making sense, send remainders to nonsense list. List must be short enough to be manually checked. Actually check before uncommenting this section.
if len(tonorm) < 50:
    for oS_tn_i in range(len(tonorm)): 
        nonsenserevs.append(tonorm[oS_tn_i])
        nonsenserevs_i.append(tonorm_i[oS_tn_i])

print("Final number of nonsense reviews: " + str(len(nonsenserevs)))
print("Final number of nonsense reviews (confirm with index number): " + str(len(nonsenserevs_i)))

dfs_final = dfs.drop(nonsenserevs_i)
print("Final cleaned row count (scale): " + str(dfs_final.shape[0]) + " (-" + str(dfsfl - dfs_final.shape[0]) + ")")

dfs_final.to_csv('rotten_tomatoes_movie_reviews_clean_scale.csv', index=False)