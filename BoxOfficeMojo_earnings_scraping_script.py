

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

# This function is a single example of how I can obtain the year, week, and
# earnings data for movies on the week page.
def test_scraping_week():
    # Check ther version of the packages being used
    print(" ")
    print("pandas version: ", pd.__version__)
    print("BeautifulSoup version: ", bs4.__version__)
    print("requests version: ", requests.__version__,'\n')


    # getting the webpage info and making sure we didn't get an error.
    response = requests.get(url="https://www.boxofficemojo.com/weekly/2025W20/?ref_=bo_wly_table_1")
    if int(response.status_code) == 200:
        print("Request successful!"+'\n')
    else:
        print("Request Unsuccessful!!!!! Please trouble shoot"+'\n')

    # Creating a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table of information on the webpage that we want
    table = soup.find('table')

    # Turn that table into a pandas dataframe
    df = pd.read_html(StringIO(str(table)))[0]
    print("An example of what the data for a specific week looks like."+'\n')
    print("Year: ",soup.title.get_text().split(" ")[1])
    print("Week: ",soup.title.get_text().split(" ")[3])
    print('\n')
    print(df)
    print('\n')
    print(df.columns)
    print('\n')

# test_scraping_week()


def test_scraping_all_weeks():
    # Check ther version of the packages being used
    print(" ")
    print("pandas version: ", pd.__version__)
    print("BeautifulSoup version: ", bs4.__version__)
    print("requests version: ", requests.__version__,'\n')


    # getting the webpage info and making sure we didn't get an error.
    response = requests.get(url="https://www.boxofficemojo.com/weekly/by-year/1978/")
    if int(response.status_code) == 200:
        print("Request successful!"+'\n')
    else:
        print("Request Unsuccessful!!!!! Please trouble shoot"+'\n')

    # Creating a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table of information on the webpage that we want
    table = soup.find('table')

    # Turn that table into a pandas dataframe
    df = pd.read_html(StringIO(str(table)))[0]
    print("An example of what the year page looks like."+'\n')
    print(df)
    print('\n')
    print(df.columns)
    print('\n')
    print(df.loc[df['Releases'] != "-"])
    print('\n')


# test_scraping_all_weeks()


# This function accepts a start and end year and scrapes together all the data
# for all the weeks in and between those years for weeks that had movies in theaters.
# This data is then deposited into a tsv file.
def scrape_boxofficemojo_weekly_earnings_webpage(start_year,end_year):

    for year in range(start_year,end_year+1):
        response_year = requests.get(url="https://www.boxofficemojo.com/weekly/by-year/"+str(year)+"/")
        df = pd.read_html(StringIO(str(BeautifulSoup(response_year.text, 'html.parser').find('table'))))[0]
        weeks = df.loc[df['Top 10 Gross'] != "-"]['Week']
        table_nums = [num+1 for num in weeks.index]
        weeks = [week for week in weeks]
        for j in range(0,len(weeks)):
            response_week = requests.get(url="https://www.boxofficemojo.com/weekly/"+str(year)+"W"+str(weeks[j])+"/?ref_=bo_wly_table_"+str(table_nums))
            soup = BeautifulSoup(response_week.text, 'html.parser')
            print("Year: ",soup.title.get_text().split(" ")[1]," Week: ",soup.title.get_text().split(" ")[3])
            df = pd.read_html(StringIO(str(soup.find('table'))))[0]

            # now i must table the data from the table and enter it into a csv file along with the week and year data. 
        





start_year = 1978
end_year = 1978
scrape_boxofficemojo_weekly_earnings_webpage(start_year,end_year)




