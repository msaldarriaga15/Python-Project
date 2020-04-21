#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 17:14:18 2020

@author: tomapavlov

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