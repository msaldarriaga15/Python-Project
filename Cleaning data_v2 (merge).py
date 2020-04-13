#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:39:38 2020

@author: marianasaldarriagaosorio
"""

## Loading and viewing the data

# Import pandas
import pandas as pd

# Read the file into a DataFrame: df
df1 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/jobs_1_26032020.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/jobs_2_26032020.csv')

#Merge Two Datasets
df_merged = df1.append(df2, ignore_index=True)

# Print the head of df
print(df_merged.head())

# Print the tail of df
print(df_merged.tail())

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

df1.to_csv("df_cleanv1.csv", index=True, encoding='utf8')
