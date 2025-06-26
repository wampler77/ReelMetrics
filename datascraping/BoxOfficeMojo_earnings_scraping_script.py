

#
# Script for scraping earnings over time for movies
# from Box Office Mojo website.
#


# packages to import
import pandas as pd
import bs4
from bs4 import BeautifulSoup # BeautifulSoup
import requests
from io import StringIO
import re
import numpy as np
import time
from datetime import datetime
import pickle

# This function gets the release numbers for every movie shown domestically in any week in the 
# interval of years given.
def retrieve_release_numbers(start_year,end_year):
    print(" ")
    start = time.time()
    # This portions loops through all the weeks in all the years in the interval selected
    # and creates a dictionary of movie release numbers and the years in which the 
    # domestic data for the movie starts
    rl_numbers = {}
    for year in range(start_year,end_year+1):
        print(year)
        response_year = requests.get(url="https://www.boxofficemojo.com/weekly/by-year/"+str(year)+"/")
        if response_year.status_code != 200:
            print("Failed request for year: ",year)
        df = pd.read_html(StringIO(str(BeautifulSoup(response_year.text, 'html.parser').find('table'))))[0]
        weeks = df.loc[df['Top 10 Gross'] != "-"]['Week']
        table_nums = [num+1 for num in weeks.index]
        weeks = [week for week in weeks]
        # Loop through the weeks in a given year
        for i in range(0,len(weeks)):
            if len(str(weeks[i])) > 1:
                response_week = requests.get(url="https://www.boxofficemojo.com/weekly/"+str(year)+
                                             "W"+str(weeks[i])+"/?ref_=bo_wly_table_"+str(table_nums))
            else:
                response_week = requests.get(url="https://www.boxofficemojo.com/weekly/"+str(year)+
                                             "W0"+str(weeks[i])+"/?ref_=bo_wly_table_"+str(table_nums))
            if response_week.status_code != 200:
                print("Failed response for year and week: ",year,weeks[i])
            soup = BeautifulSoup(response_week.text, 'html.parser')
            current_rl_numbers = [str(r).split('/')[2] for r in soup.find('table').find_all('td', attrs={"class":"a-text-left mojo-field-type-release mojo-cell-wide"})]
            for rl_num in current_rl_numbers:
                if rl_num not in rl_numbers:
                    rl_numbers[rl_num] = year
    
    print(" ")
    print("Number of rl numbers collected: ", len(rl_numbers))
    print(" ")

    file1 = open('C:/Users/micha/OneDrive/Documents/Grad School 3rd year/Summer 2025/Project Codes/datasets/'
                 +str(start_year)+'-'+str(end_year)+'_rl_numbers.txt','w')
    for rl_num in rl_numbers:
        file1.write(str(rl_num)+'\t'+str(rl_numbers[rl_num])+'\n')
    file1.close()

    print("Time to collect all rl numbers:",round((time.time()-start)/60,2))

# This function accepts a start and end year and scrapes together all the grossing data
# by week for every movie released in and between the given years. Only the domestic 
# original release data is collected. 
def scrape_boxofficemojo_weekly_earnings_webpage(start_year,end_year):
    print(" ")
    start = time.time()

    # set up dicitonary to collect all data and turn into dataframe to be saved
    columns = ['Movie Title','Rank','Gross ($)','Theater Number',
               'Change in Theater Number','Gross to Date','Week','Date']
    data_dict = {}
    for column in columns:
        data_dict[column] = []
    
    # get the dictionary of rl numbers
    rl_numbers = {}
    file1 = open('C:/Users/micha/OneDrive/Documents/Grad School 3rd year/Summer 2025/Project Codes/datasets/'
                 +str(start_year)+'-'+str(end_year)+'_rl_numbers.txt','r')
    A = "Bessie"
    while A != "":
        A = file1.readline()
        if A == "":
            break
        A = A.split('\t')
        rl_numbers[A[0]] = A[1].strip('\n')
    file1.close()
    print("Number of movies:",len(rl_numbers))
    print(" ")
    
    # This portion loops through the rl#'s going to each movies page and obtaining 
    # the data from the page.
    count = 0
    possible_years = [i for i in range(1977,2026)]
    for rl_num in rl_numbers:
        # connect to webpage
        response_movie = requests.get(url="https://www.boxofficemojo.com/release/"+rl_num+"/weekly/?ref_=bo_rl_tab#tabs")
        if response_movie.status_code != 200:
            print("Failed request for movie: ",rl_num)
        soup = BeautifulSoup(response_movie.text, 'html.parser')

        # get movie release year to add to title
        A = [str(x) for x in soup.find_all('div', attrs={'class':'a-section a-spacing-none'}) if "Release Date" in str(x)]
        options = []
        for x in A:
            for i in range(4,len(x)):
                if x[i-4:i].isdigit() == True:
                    options += [int(x[i-4:i])]
        if len(options) < 1:
            print("ERROR: NO RELEASE YEAR FOUND,",re.sub(' - Box Office Mojo','',soup.title.get_text()))
            print(A)
        else:
            release_year = str(np.min(options))
            movie_title = re.sub(' - Box Office Mojo','',soup.title.get_text())+" ("+release_year+")-"+str(rl_num)
            if int(release_year) not in possible_years:
                print("ERROR: RELEASE YEAR NOT IN POSSIBLE YEARS,",movie_title,",",rl_num)
            
            # set current year to the year that the data starts
            current_year = rl_numbers[rl_num]

            #print(movie_title,current_year)

            # get the information from the webpage into a dataframe and then collect 
            # the desired info and store it in the data dictionary
            df = pd.read_html(StringIO(str(soup.find('table'))))[0]
            movie_title_list = [movie_title for i in range(0,len(df))]
            A = df['Rank']
            rank_list =  []
            for i in range(0,len(A)):
                if A[i] == "-":
                    rank_list += [np.nan]
                else:
                    rank_list += [int(A[i])]
            A = df['Weekly']
            gross_list = []
            for i in range(0,len(A)):
                if A[i] == "-":
                    gross_list += [np.nan]
                else:
                    gross_list += [int(re.sub(',','',A[i]).strip('$'))]
            A = df['Theaters']
            theaters_list = []
            for i in range(0,len(A)):
                if A[i] == "-":
                    theaters_list += [np.nan]
                else:
                    theaters_list += [int(A[i])]
            A = df['Change']
            theater_change_list = []
            for i in range(0,len(A)):
                if A[i] == "-":
                    theater_change_list += [np.nan]
                else:
                    theater_change_list += [int(A[i])]
            A = df['To Date']
            gross_to_date_list = []
            for i in range(0,len(A)):
                if A[i] == "-":
                    gross_to_date_list += [np.nan]
                else:
                    gross_to_date_list += [int(re.sub(',','',A[i]).strip('$'))]
            A = df['Week']
            week_list = []
            for i in range(0,len(A)):
                if A[i] == "-":
                    week_list += [np.nan]
                else:
                    week_list += [int(A[i])]
            A = list(df['Date'])
            dates_list = []
            for i in range(0,len(A)):
                B = A[i].split('-')[0].split(' ')
                if B[0] == "Feb" and B[1] == "29":
                    dates_list += [B[0]+" "+str(int(B[1])-1)]
                else:
                    dates_list += [B[0]+" "+B[1]]
            years_to_append = [current_year]
            for i in range(1,len(dates_list)):
                if (datetime.strptime(dates_list[i],"%b %d")-datetime.strptime(dates_list[i-1],"%b %d")).days < 0:
                    current_year = str(int(current_year)+1)
                if int(current_year) not in possible_years:
                    print("ERROR dates,",movie_title,",",current_year)
                years_to_append += [current_year]
            dates_list_final = []
            for i in range(0,len(dates_list)):
                dates_list_final += [datetime.strptime(dates_list[i]+" "+years_to_append[i],"%b %d %Y")]
            data_dict['Movie Title'] += movie_title_list
            data_dict['Rank'] += rank_list
            data_dict['Gross ($)'] += gross_list
            data_dict['Theater Number'] += theaters_list
            data_dict['Change in Theater Number'] += theater_change_list
            data_dict['Gross to Date'] += gross_to_date_list
            data_dict['Week'] += week_list
            data_dict['Date'] += dates_list_final

            count += 1
            if count%int(len(rl_numbers)/100) == 0:
                print(int((count/len(rl_numbers))*100),"%")


    # This portion creates a pandas dataframe and saves it in a text file
    df_data = pd.DataFrame(data_dict)
    print("number of movies:",len(df_data['Movie Title'].unique()))
    df_data.to_csv('C:/Users/micha/OneDrive/Documents/Grad School 3rd year/Summer 2025/Project Codes/datasets/'
                   +str(start_year)+"-"+str(end_year)+".txt",
                   sep = '\t',
                   encoding = 'utf-8',
                   index = False)

    pickle.dump(df_data, open( "1977-2025.p", "wb" ) )

    print(" ")
    print("Time to collect data:",round((time.time()-start)/60,3),"minutes")
    print(" ")
        

start_year = 1977
end_year = 2025
retrieve_release_numbers(start_year,end_year)
scrape_boxofficemojo_weekly_earnings_webpage(start_year,end_year)











