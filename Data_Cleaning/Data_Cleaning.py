# -*- coding: utf-8 -*-
## Import packages
import pandas as pd
import numpy as np

import re

import matplotlib.pyplot as plt

import nltk

from nltk.corpus import stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

pip install wordcloud
from wordcloud import WordCloud

conda install -c conda-forge spacy
from spacy.lang.en.stop_words import STOP_WORDS

import collections
from collections import Counter

conda install -c conda-forge textblob
from textblob import TextBlob
from textblob import Word

## Load and observe the data

# Read the file into a DataFrame
df1 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/jobs_data+analyst.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/jobs_data+scientist.csv')

# Merge two Datasets
df_merged = df1.append(df2, ignore_index=True)

# Print the head of df
print(df_merged.head())

# Print the tail of df
print(df_merged.tail())

# Print the shape of df
print(df_merged.shape)

# Print the columns of df
print(df_merged.columns)

# Print the info of df
print(df_merged.info())

## Rename the columns

# Dictionary columns names
new_names = {'Unnamed: 0': 'Obs', 
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

def rename_col(df_merged):
    '''
    We want to rename the columns of the merged data.
    The result will be a data with proper and informative labels.
    '''
    df_merged_rename = df_merged.rename(columns=new_names, inplace=True)
    return df_merged_rename

df_merged_rename = rename_col(df_merged)

# Check and see new columns 
print(df_merged.columns)

## Dealing with the missing values

'''
We want to observe for which cells we couldn't get information from the web scraping.
We take a look at all the data frame. We realize the missing values are defined as a string
'NOT_FOUND'.
The cells with no information will be marked as True. 
'''

print((df_merged[['City','Search','Job_title',
           'Company_name','Location',
           'Rating','Website',
           'Days_posted',
           'Job_description',
           'Location2']] == 'NOT_FOUND'))


def mark_nan_values(df_merged):
    '''
    We want to mark 'NOT_FOUND' as missing value or NaN. 
    All missing values (before strings) will be interpreted as NaN by Python.
    '''
    df_merged[['Company_name', 'Location','Rating','Job_description','Location2']] = df_merged[['Company_name', 'Location', 'Rating','Job_description', 'Location2']].replace({'NOT_FOUND': np.NaN}) # columns without information in some cells 
    return df_merged

df_merged_NaN = mark_nan_values(df_merged)


# We count the number of NaN values in each column of the data frame (also check)
print(df_merged.isnull().sum())


def drop_col(df_merged):
    '''
    We drop the column 'Location' since it has many missing values: drop 'Location'
    '''
    df_merged_drop = df_merged.drop(['Location'], axis=1)
    return df_merged_drop

df_merged_drop = drop_col(df_merged)

print(df_merged_drop.columns)


# Organize the shape of the data
print(df_merged_drop.index)

'''
Our index is well specified, and it's the column observation.
'''


## Data types of our database

print(df_merged_drop.dtypes)

def change_dtypes(df_merged_drop):
    '''
    We want to change some dtypes to save memory and work with numerical 
    format.
    The columns 'Days_posted' and 'Rating' are defined as objects
    that we want to transform into integers.
    We will get these columns as numbers and we will save memory.
    '''
    df_merged_drop['Days_posted_2'] = df_merged_drop['Days_posted'].str.extract('(\d+)') # Find the numeric values
    df_merged_drop['Days_posted_2'] = pd.to_numeric(df_merged_drop['Days_posted_2'], errors='coerce') # Convert into float

    df_merged_drop['Rating'] = df_merged_drop['Rating'].str.extract('(\d+)')
    df_merged_drop['Rating'] = pd.to_numeric(df_merged_drop['Rating'], errors='coerce')
    return df_merged_drop

df_merged_types = change_dtypes(df_merged_drop)

print(df_merged_types.info())

'''
The number of missing values in the column decreased. 
'''

# Summary statistics of 'Days_posted_2' and ' Rating'
df_merged_types.describe()

# Visualizing 'Days_posted_2' with histograms
df_merged_types['Days_posted_2'].plot(kind='hist',
    xtitle='Days',
    linecolor='black',
    yTitle='count',
    title='Days posted Distribution') 

# Visualizing 'Rating' with histograms
df_merged_types['Rating'].plot(
    kind='hist',
    xTitle='rating',
    linecolor='black',
    yTitle='count',
    title='Review Rating Distribution')
 
## Separate 'Location2' 

# New data frame with split value columns 
new = df_merged_types['Location2'].str.split(" ", n = 1, expand = True) 
  
# Making separate first name column from new data frame 
df_merged_types['Postal_code_Berlin']= new[0] 
df_merged_types['Postal_code_Berlin'] = pd.to_numeric(df_merged_types['Postal_code_Berlin'], downcast='integer', errors='coerce')

'''
Here we want an integer not a float
'''

## Output 'clean_v1' data to a CSV file

# To avoid character issues, use utf8 encoding for input/output.

df_merged_types.to_csv("data_clean.csv", index=True, encoding='utf8')


#### Continue data cleaning (post midterm report)

data_clean = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/data_clean.csv')

## Duplicates

# Check for duplicate rows based on all columns

def check_duplicates(data_clean):
    '''
    This function is to find duplicate rows. 
    It returns a Boolean Series with True value for each duplicated row.
    The first argument 'subset' specifies the column labels used for duplication check. 
    We did not specify it since we want to check all columns labels for finding 
    duplicate rows. 
    The second argument keep denotes the occurrence which should be marked as duplicate.
    It’s value can be {‘first’, ‘last’, False}. In this case, we specify false because 
    we want all duplicates be marked as True, and the default value is
    'first’ which mark as True all duplicates except their first occurrence.
    Result: no duplicate rows in our data frame.
    ''' 
    duplicate_rowsdf = data_clean[data_clean.duplicated(keep=False)]
    return duplicate_rowsdf

duplicate_rowsdf = check_duplicates(data_clean)

print("All Duplicate Rows based on all columns are :")
print(duplicate_rowsdf) 

# Length of data frame
len(data_clean)

# Number of values per columns
data_clean.count()

# Recall data types of our base
print(data_clean.dtypes)


def categorical_col(data_clean):
    '''
    Describe categorical columns of type np.object. 
    We are interested in describing the jobs offered and by which companies.
    For the description of non-numerical columns we must be explicitly specify
    include=object (the object data type).
    Transpose() is used for a better format of the result table.
    The data set (data_clean) contains 1791 job posts offering 528 different job positions
    from 314 companies. Senior Data Analyst is the job position most offered and Zalando SE
    is the company offering more jobs at the date (march 2020).
    '''
    data_clean_describe = data_clean[['Job_title', 'Company_name']].describe(include=object).transpose()
    return data_clean_describe

data_clean_describe = categorical_col(data_clean)

print(data_clean_describe)


def group_by_company(data_clean):
    '''
    We want to group by Company and count different job positions offered and posts
    '''
    cat_data_clean = data_clean.groupby('Company_name') \
                .agg({'Job_title':pd.Series.nunique,
                      'Unnamed: 0': pd.Series.nunique})\
                .rename(columns = {'Job_title':'num_job_title',
                                   'Unnamed: 0': 'num_job_posts'})\
                .sort_values('num_job_title', ascending=False)
    return cat_data_clean
  
cat_data_clean = group_by_company(data_clean)

print(cat_data_clean)    
   
              
def describe_by_company(cat_data_clean):
    '''
    We want to take a look at the summary description of the new subset we create
    previously. 
    Looking at the summary of the data we observe that the mean average of job posts
    per company is almost 6. We realize that 75% of the companies offer less than 2 job posts. 
    Also, 75% of the companies only offer two types of jobs (job titles) for data scientists
    and data analysts. 
    '''
    cat_data_clean_describe = cat_data_clean.describe()
    return cat_data_clean_describe
    
cat_data_clean_describe = describe_by_company(cat_data_clean)

print(cat_data_clean_describe)


def features_by_company(cat_data_clean):
    '''
    We want to observe the supply job market extracted from our web scrapping. 
    This function allow us to see the companies that offered most and less
    job positions and job titles.  
    Results:
    1. Of 314 companies that offered job positions in March 2020, 191 companies offered only one job position. 
    2. 214 companies only offered one type of job title for data scientists and data analysts. 
    3. Zalando SE is the branch of this company that is offering more job positions
    (229) in March 2020. Zalando is also the company offering the more different 
    job titles (32) to data analysts and data scientists in the labor market, 
    based in our web scrapping.
    '''
    companies_1offer = cat_data_clean[cat_data_clean['num_job_posts'] == 1 ].index # Get names of companies that only offer 1 type of job position
    companies_1title = cat_data_clean[cat_data_clean['num_job_title'] == 1 ].index # Get names of companies that only offer 1 job title
    companies_maxoffer = cat_data_clean[cat_data_clean['num_job_posts'] == 229 ].index # Get company that offer the maximum of job positions
    companies_maxtitle = cat_data_clean[cat_data_clean['num_job_title'] == 32 ].index # Get company that offer the maximum of job titles
    return features_by_company

features_by_company = features_by_company(cat_data_clean)

print(features_by_company)


def select_companies(cat_data_clean):
    '''
    We select the most relevant companies to visualize better our results (too many companies).
    The .loc indexer selects data in a different way than just the indexing operator. 
    It can select subsets of rows or columns. It can also simultaneously select subsets 
    of rows and columns. Most importantly, it only selects data by the LABEL of the rows 
    and columns.
    We will have two different subsets
    '''
    chart_company = cat_data_clean.loc[cat_data_clean['num_job_posts'] > 18]
    return chart_company

chart_company = select_companies(cat_data_clean)

'''
We plot the main features of these subsets by company that we created. 
The results will be shown in histogramms. 
'''
chart_company[['num_job_posts']].plot(kind = 'bar', figsize=(7,4)) # Bar chart of number of job posts by company
    
chart_company[['num_job_title']].plot(kind = 'bar', figsize=(7,4)) # Bar chart of number of types of jobs offered by company



### Job_description column analysis (text analysis)

data_clean_text = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/final_dataset.csv')

print(data_clean_text.columns)


def create_subset_data_clean(data_clean_text):
    '''
    We create a new subset of the big dataframe to get a smaller data frame to work on.
    We specify the columns we want to drop. 
    '''
    sub_data_clean_text = data_clean_text.drop(['Unnamed: 0', 'Id', 'City', 'Search',
                                  'Rating', 'Website', 'Days_posted',
                                  'Location2', 'Days_posted_2',
                                  'Postal_code_Berlin', 'python', ' r', 'java',
                                  'sas', 'sql', 'stata', 'spss', 'ruby',
                                  'javascript', 'php', 'skills_as_list', 'skill_clean'], axis=1)
    return sub_data_clean_text

sub_data_clean_text = create_subset_data_clean(data_clean_text)

print(sub_data_clean_text.columns)


def create_subset_data_eng(sub_data_clean_text):
    '''
    This function will keep the rows where english is the language.
    We will get a subset with only job offers in english.
    '''
    eng_data_clean_text = sub_data_clean_text[sub_data_clean_text.language == 'English']
    return eng_data_clean_text

eng_data_clean_text = create_subset_data_eng(sub_data_clean_text)

print(eng_data_clean_text)

# Histogram frequency companies 
eng_data_clean_text['Company_name'].value_counts(dropna=False)[:20].plot(kind='bar')

# Save data base with only job offers in english
eng_data_clean_text.to_csv("eng_data_clean_text.csv", index=True, encoding='utf8') 

    
def basic_feature_extraction(eng_data_clean_text):
    '''
    1. We use the split function. We asume that the job descriptions with more words have
    detailed information about the job offers for data scientists and data analysts.
    2. We calculate the number of characters in each job description. 
    This is done by calculating the length of the description.
    3. One of the first steps is to remove the stopwords from our text (see below Basic pre-processing),
    but first we count them. 
    '''
    eng_data_clean_text['word_count'] = eng_data_clean_text['Job_description'].apply(lambda x: len(str(x).split(" "))) # Number of words
    eng_data_clean_text['char_count'] = eng_data_clean_text['Job_description'].str.len() # Number of characters (it includes spaces)
    eng_data_clean_text['stopwords'] = eng_data_clean_text['Job_description'].apply(lambda x: len([x for x in x.split() if x in stop])) # Number of stopwords
    return eng_data_clean_text

eng_data_clean_text = basic_feature_extraction(eng_data_clean_text)
    
print(eng_data_clean_text[['Job_description','word_count']].head())
print(eng_data_clean_text[['Job_description','char_count']].head())
print(eng_data_clean_text[['Job_description','stopwords']].head())


def basic_pre_processing(eng_data_clean_text):
    '''
    We clean the text data in order to obtain better results. For this we will do some
    basic pre-processing steps on our data. This is essential to help us reduce
    vocabulary. The features produced are more effective.
    The first pre-processing step that we did is to transform the 'Job description' text
    into lower case. This avoids having multiple copies of the same words that start 
    with a lower case or upper case.
    Second, it is important to remove punctuation since it doesn't add any extra information 
    while treating text data. Hence, if we remove it we can schrink the size of the data. 
    Third, we remove the stopwords from our text.
    Finally, we correct the spelling to reduce multiple copies of words. 
    To do this we will use the textblob library already imported.
    Result: clean text data in the column 'Job_description'
    '''
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join(x.lower() for x in x.split())) # Transfor text into lower case
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].str.replace('[^\w\s]','') # Remove punctuation
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop)) # Removal of stopwords
    eng_data_clean_text['Job_description'][:5].apply(lambda x: str(TextBlob(x).correct())) # Spelling correction
    return eng_data_clean_text

process_eng_data_text = basic_pre_processing(eng_data_clean_text)

print(process_eng_data_text['Job_description'].head())

def lemmatization(eng_data_clean_text):
    '''
    We do lemmatization to group together words which do not have the same root. 
    That way they are processed as one item.
    '''
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    return lemmatization()

lemm_eng_data_clean_text = lemmatization(eng_data_clean_text)

print(eng_data_clean_text['Job_description'].head())


def frequent_words(process_eng_data_text):
    '''
    The most occurring words are: data, team, experience, business, work, product, working, teams,
    development, skills. We decide not to remove them since they are interesting to describe
    what job offers are requesting.
    '''
    freq_description = pd.Series(' '.join(eng_data_clean_text['Job_description']).split()).value_counts()[:20]
    freq_description_list = ['teams', 'strong', 'new', 'company', 'work', 'working'] # List some frequent words not relevant
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join(x for x in x.split() if x not in freq_description_list))
    return freq_description


def rare_words(process_eng_data_text):
   '''
   It's important to remove rarely occurring words from the text. 
   Because they’re so rare, the association between them and other words
   is dominated by noise. 
   Here we count and remove the rare words (in a list).
   '''
   rare_description = pd.Series(' '.join(eng_data_clean_text['Job_description']).split()).value_counts()[-10:]
   rare_description_list = list(rare_description.index) # List rare words
   eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join(x for x in x.split() if x not in rare_description_list))
   return rare_description

rare_description = rare_words(process_eng_data_text)

print(rare_description)
print(eng_data_clean_text['Job_description'].head())


def my_tokenizer(text):
    '''
    We define the function my_tokenizer . As we are working with
    a space-separated list of nouns, we can simply tokenize by splitting the string.
    '''
    return text.split() if text != None else[]

def tokenization(eng_data_clean_text):
    '''
    Tokenization refers to dividing the text into a sequence of words or sentences.
    Any analysis of word or token frequencies requires a list of words. 
    The generation of a single list of tokens can be done by the following 
    sequence of operations:
    1. Select the column of the data frame
    2. Map each document to a list of tokens
    The map operation applies a function, in our case my_tokenizer, 
    to all the values in a column and transforms it into a list of tokens. 
    3. Concatenate these lists of tokens into a single list. The sum() operation computes the total sum over all values, which is for lists
    just the concatenation.
    '''
    tokens_description = eng_data_clean_text.Job_description.map(my_tokenizer).sum() 
    return tokens_description

tokens_description = tokenization(eng_data_clean_text)

print(tokens_description)


def count_words(tokens_description):
    '''
    We count frequencies with a counter. 
    We keep the 20 most common words.
    '''
    counter_description =  Counter(tokens_description) 
    return

def remove_stopwords_tokens(tokens_description):
    '''
    Remove stopwords from the list of tokens
    '''
    return [t for t in tokens_description if t not in STOP_WORDS]

def recount_words(tokens_description):
    '''
    Rebuild counter without stopwords
    '''
    counter_description2 = Counter(remove_stopwords_tokens(tokens_description))
    return counter_description2

counter_description2 = recount_words(tokens_description)

# Word cloud more used words in column Job description
def wordcloud(counter_description2):
    '''
    Word clouds: visualization word frequency
    '''
    wc = WordCloud( width=1200, height=800,
                    background_color="white",
                    max_words=200)
    wc.generate_from_frequencies(counter_description2)
    
    # Plot
    
    plt.figure(figsize=(20,10))
    plt.imshow(wc , interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

wordcloud(counter_description2)

# Word cloud companies

tokens_company = eng_data_clean_text.Company_name.map(my_tokenizer).sum()

tokens_company

counter_company =  Counter(tokens_company)
counter_company.most_common(20)

def remove_stopwords(tokens_company):
    """Remove stopwords from the list of okens"""
    return [t for t in tokens_company if t not in STOP_WORDS]

counter_company2 = Counter(remove_stopwords(tokens_company))
counter_company2

def wordcloud(counter_company2):
    '''Wordcloud'''
    wc = WordCloud( width=1200, height=800,
                    background_color="white",
                    max_words=200)
    wc.generate_from_frequencies(counter_company2)
    
    # Plot
    
    plt.figure(figsize=(20,10))
    plt.imshow(wc , interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

wordcloud(counter_company2)

# Save data base with only job offers in english
eng_data_clean_text.to_csv("process_text_data.csv", index=True, encoding='utf8') 




