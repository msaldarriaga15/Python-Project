# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:45:33 2020

@author: Toma, Mariana, Andrea, Aline
"""

# import packages
import requests
import pandas as pd
import time 


# import packages
# Beautiful Soup is a Python library for pulling data out of HTML and XML files. 

from selenium import webdriver
import bs4
from bs4 import BeautifulSoup

# get soup object
def get_soup(text):
	return BeautifulSoup(text, "lxml", from_encoding="utf-8")

# extract company
def extract_company(div): 
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
        for b in company:
            return (b.text.strip())
    else:
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            return (span.text.strip())
    return 'NOT_FOUND'

# extract job location
def extract_location(div):
    for span in div.findAll('span', attrs={'class': 'location'}):
        return (span.text)
    return 'NOT_FOUND'

# extract job title
def extract_job_title(div):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['title'])
    return('NOT_FOUND')

# extract link of job description 
def extract_link(div): 
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['href'])
    return('NOT_FOUND')
    
# extract rating
def extract_rating(div):
    for span in div.findAll('span', attrs={'class': 'ratingsContent'}):
        return (span.text.strip())
    return 'NOT_FOUND'

# extract date of job when it was posted
def extract_date(div):
    try:
        spans = div.findAll('span', attrs={'class': 'date'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

# extract full job description from link
def extract_fulltext(url):
    try:
        page = requests.get('https://de.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': 'jobsearch-jobDescriptionText'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

# extract location
def extract_location2(url):
    try:
        page = requests.get('https://de.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('span', attrs={'class': 'jobsearch-JobMetadataHeader-iconLabel'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

# extract type of employment/salary
def extract_employment(url):
    try:
        page = requests.get('https://de.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': 'jobsearch-JobMetadataHeader-iconLabel'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

# write logs to file
def write_logs(text):
    # print(text + '\n')
    f = open('log.txt','a')
    f.write(text + '\n')  
    f.close()

# limit results per sity
max_results_per_city = 500

# db of city 
city_set = ['Berlin']

# job roles
job_set = ['data+analyst','data+scientist']


# file num
file = 1

# from where to skip
SKIPPER = 0

# loop on all cities
for city in city_set:
    
    # for each job role
    for job_qry in job_set:
        
        # count
        cnt = 0
        startTime = time.time()

        # skipper
        if(file > SKIPPER):
        
            # dataframe
            df = pd.DataFrame(columns = ['unique_id', 'city', 'job_qry','job_title', 'company_name', 'location', 'rating', 'link', 'date', 'full_text', 'location_full_text'])
        
            # for results
            for start in range(0, max_results_per_city, 10):

                # get dom 
                page = requests.get('https://de.indeed.com/jobs?q=' + job_qry +'&l=' + str(city) + '&start=' + str(start))

                #ensuring at least 1 second between page grabs                    
                time.sleep(1)  

                #fetch data
                soup = get_soup(page.text)
                divs = soup.find_all(name="div", attrs={"class":"row"})
                
                # if results exist
                if(len(divs) == 0):
                    break

                # for all jobs on a page
                for div in divs: 

                    #specifying row num for index of job posting in dataframe
                    num = (len(df) + 1) 
                    cnt = cnt + 1

                    #job data after parsing
                    job_post = [] 

                    #append unique id
                    job_post.append(div['id'])

                    #append city name
                    job_post.append(city)

                    #append job qry
                    job_post.append(job_qry)

                    #grabbing job title
                    job_post.append(extract_job_title(div))

                    #grabbing company
                    job_post.append(extract_company(div))

                    #grabbing location name
                    job_post.append(extract_location(div))

                    #grabbing rating
                    job_post.append(extract_rating(div))

                    #grabbing link
                    link = extract_link(div)
                    job_post.append('https://de.indeed.com' + extract_link(div))

                    #grabbing date
                    job_post.append(extract_date(div))

                    #grabbing full_text
                    job_post.append(extract_fulltext(link))
                    
                    #grabbing location from full job description
                    job_post.append(extract_location2(link))
                    
                    #grabbing location from full job description
                    #job_post.append(extract_employment(link))

                    #appending list of job post info to dataframe at index num
                    df.loc[num] = job_post
                    
                #debug add
                write_logs(('Completed =>') + '\t' + city  + '\t' + job_qry + '\t' + str(cnt) + '\t' + str(start) + '\t' + str(time.time() - startTime) + '\t' + ('file_' + str(file)))

            #saving df as a local csv file 
            df.to_csv('jobs_' + str(file) + '.csv', encoding='utf-8')
        
        else:

            #debug add
            write_logs(('Skipped =>') + '\t' + city  + '\t' + job_qry + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(time.time() - startTime) + '\t' + ('file_' + str(file)))
        
        # increment file
        file = file + 1
        

## Loading and viewing the data

# Import pandas
import pandas as pd

# Read the file into a DataFrame: df
df = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/jobs_2_26032020.csv')

# Print the head of df
print(df.head())

# Print the tail of df
print(df.tail())

# Print the shape of df
print(df.shape)

# Print the columns of df
print(df.columns)

# Print the info of df
print(df.info())

## Rename the columns

# Dictionary
new_names = {'Unamed: 0': 'Obs', 
             'unique_id': 'Id',
             'city': 'City', 
             'job_qry': 'Search',
             'job_title': 'Job_title',
             'company_name': 'Company_name',
             'location': 'Location',
             'rating': 'Rating',
             'link': 'Website',
             'date': 'Days_posted',
             'full_text': 'Job_description',
             'location_full_text': 'Location2'}

df.rename(columns=new_names, inplace=True)

# Check
df.head()
print(df.columns)

## Looking for missing values
print((df[['City','Search','Job_title',
           'Company_name','Location',
           'Rating','Website',
           'Days_posted',
           'Job_description',
           'Location2']] == 'NOT_FOUND').sum)

# Mark 'NOT_FOUND' as missing value or NaN
import numpy as np

df[['Location', 'Rating']] = df[['Location', 'Rating']].replace({'NOT_FOUND': np.NaN})

# Count the number of NaN values in each column
print(df.isnull().sum())

# 'Location' has many missing values: drop 'Location'
df1 = df.drop(['Location'], axis=1)

# Organize the shape of the data
print(df1.index)

'''
Our index is well specified, and it's the column observation.
'''

## Data types of our database
print(df1.dtypes)

# Import the regular expression module
import re

# Find the numeric values: 'Days posted' and convert into float
df1['Days_posted_2'] = df1['Days_posted'].str.extract('(\d+)')
df1['Days_posted_2'] = pd.to_numeric(df1['Days_posted_2'], downcast='integer', errors='coerce')

# Find the numeric values: 'Rating' and convert into float
df1['Rating'] = df1['Rating'].str.extract('(\d+)')
df1['Rating'] = pd.to_numeric(df1['Rating'], downcast='integer', errors='coerce')

print(df1.info())


'''
The number of missing values in the column decreased. 
'''

# Summary statistics of 'Days_posted_2' and ' Rating'
df1.describe()

# Visualizing 'Days_posted_2' with histograms
import matplotlib.pyplot as plt

df1['Days_posted_2'].plot(
    kind='hist',
    xTitle='Days',
    linecolor='black',
    yTitle='count',
    title='Days posted Distribution') 

# Visualizing 'Rating' with histograms
import matplotlib.pyplot as plt

df1['Rating'].plot(
    kind='hist',
    xTitle='rating',
    linecolor='black',
    yTitle='count',
    title='Review Rating Distribution')
 
## Separate 'Location2' 

# New data frame with split value columns 
new = df1['Location2'].str.split(" ", n = 1, expand = True) 
  
# Making separate first name column from new data frame 
df1['Postal_code_Berlin']= new[0] 
df1['Postal_code_Berlin'] = pd.to_numeric(df1['Postal_code_Berlin'], downcast='integer', errors='coerce')

'''
Here we want an integer not a float
'''

## Frequency counts

# Job_title
df1.Job_title.value_counts(dropna=False)

# Company_name
df1.Company_name.value_counts(dropna=False)

## Output 'clean_v1' data to a CSV file
# To avoid character issues, use utf8 encoding for input/output.

df1.to_csv("Data2_Clean.csv", index=True, encoding='utf8')


import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd

#Define the spacy_langdetect function
nlp = spacy.load("en_core_web_sm")

#From https://github.com/Abhijit-2592/spacy-langdetect
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
text = "This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. Yo me divierto todos los días en el parque. Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."
doc = nlp(text)

#Document level language detection. Think of it like average language of document!
print(doc._.language)

#Sentence level language detection
for i, sent in enumerate(doc.sents):
    print(sent, sent._.language)

#Example from our dataset to test the function
column_de = """
"Im Bereich Planung und Bau - Investitionssteuerung (PB-I) sind wir fÃ¼r die kosten- und termingerechte Steuerung der NetzbaumaÃŸnahmen und das dezentrale Controlling inklusive Personalcontrolling fÃ¼r ca. 650 Mitarbeiter verantwortlich. HierfÃ¼r (Standort: Neue JÃ¼denstraÃŸe 1 in 10179 Berlin) suchen wir ab sofort VerstÃ¤rkung.
Was Sie bei uns bewegen
Sie verantworten unsere Prognosemodelle auf Basis frequentistischer und Bayesianischer Statistik
Sie leiten die Projektgruppe fÃ¼r Prognosen und Prognosemethoden
Sie konzeptionieren unsere Datenmodellierung und entwickeln bestehende Datenmodelle weiter
Sie stellen unser PB-Reporting zentraler Controlling-Inhalte auf webbasiertes Online-Reporting um
Behinderte Menschen werden bei gleicher Eignung bevorzugt. Da wir uns Chancengleichheit und die berufliche FÃ¶rderung von Frauen zum Ziel gesetzt haben, sind wir besonders an Bewerbungen von Frauen interessiert. Bewerbungen von Menschen mit Migrationshintergrund sind ausdrÃ¼cklich erwÃ¼nscht. Bitte senden Sie Ihre vollstÃ¤ndigen Bewerbungsunterlagen bis zum 30.04.2020 unter Angabe der Job-ID 40/2020 an nachfolgende Anschrift. Unterlagen, die Sie online einreichen, konvertieren Sie bitte zu einem PDF-Dokument (inkl. Anschreiben, Lebenslauf und Zeugnissen)."
"""

#Import dataset 1
df = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/jobs_1_26032020.csv')

#Create New Column
def detect_lang(x):
    translate = nlp(str(x)[:200])._.language
    return (translate['language'],translate['score'])

df['language'] = df['full_text'].apply(lambda x: nlp(str(x)[:200])._.language['language'])

#Check the new column
df.head()

#Generate Histogram
df['language'].value_counts().plot(kind='bar')

#Import dataset 2
data = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/Data2_Clean.csv')

#Create New Column
def detect_lang(x):
    translate = nlp(str(x)[:200])._.language
    return (translate['language'],translate['score'])

data['language'] = data['Job_description'].apply(lambda x: nlp(str(x)[:200])._.language['language'])

#Check the new column
data.head()

#Generate Histogram
data['language'].value_counts().plot(kind='bar')


import streamlit as st
import pandas as pd

### 1st task ### >> Create an user interface with a dropdown menu for collecting user's interface

#Load the excel file and read it as a table. We used a mockdataset with only 100 entries at this point.
def load_data():
    df = pd.read_csv('mock_dataset.csv',sep=',') 
    return df

df = load_data()

# Create a dropdown menu, which reads the Column "Language" in the dataset and provides the possible values 
# for the user. # We are using here "selectbox" assuming that the user can only click on one of the languages - german or 
# english.
language_user = st.sidebar.selectbox("1. Select your preferred language: ", df['Language'].unique())

# Regarding the skills, we still do not have in the database a column with all the skills required by each job
# ads. Therefore, we basically created manually a list with 10 skills, named "hardcoded_skills"
# We are using "multiselect" rather than "selectbox" assuming that the user want to select more than one skills .
hardcoded_skills = ['Machine Learning','Data Mining','Python','R','SQL','Java','Django','C','Oracle','ETL']
skills = st.sidebar.multiselect("2. Select your skills:", hardcoded_skills)

### 2nd task ## >> Display a recommendation list

#Filter the dataset by "Language"
filtered_df = df[df["Language"] == language_user]

#Create a header in the page
st.header('Here is the list of your best matching job ads')

#Change the format and the design of the list. # ** is used to t to turn it bold
for job_index, line in enumerate(filtered_df.itertuples()):
    st.markdown('### {}. {} at {} ' .format(job_index + 1, line.job_title, line.company_name)) 
    st.markdown('**Skills:** {}'.format(line.Skills))
    st.markdown('Click [here]({}) to apply'.format(line.link))