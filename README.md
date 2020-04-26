# Python-Project
Project for the class "GRAD-E1326: Python Programming for Data Scientists"

This project was divided into 4 main parts and it will be documented accordingly. 

## 1. Web Scraping

#### 1.1. How to run this script

You can find the code [here](https://github.com/Andrea-Giuliani/Python-Project/blob/master/Web_Scraping/web%20scraper_indeed_jobs.py)

#### 1.2. What the script does?

This module scrapes data science and data analyst job ads in the city of Berlin from https://de.indeed.com/. The script scrapes and parses the information into different fields, including company name, company rating, job title, job description, date of posting, and link to the full description. Finally, after information is scraped and parsed, two csv files are generated for the two respective job queries. Below are shown the main functions: 

```python
def extract_company(div): 
    """This function extracts the company name from the results page.
    
    """
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
        for b in company:
            return (b.text.strip())
    else:
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            return (span.text.strip())
    return 'NOT_FOUND'
    
def extract_location(div):
    """This function extracts the job location from the results page.
    
    """
    for span in div.findAll('span', attrs={'class': 'location'}):
        return (span.text)
    return 'NOT_FOUND'

def extract_job_title(div):
    """This function extracts the job title from the results page.
    
    """
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['title'])
    return('NOT_FOUND')

def extract_link(div):
    """This function extracts the link to the full job description from the results page.
    
    """
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['href'])
    return('NOT_FOUND')
    
def extract_rating(div):
    """This function extracts the comapny rating (if there is one) from the results page.
    
    """
    for span in div.findAll('span', attrs={'class': 'ratingsContent'}):
        return (span.text.strip())
    return 'NOT_FOUND'

def extract_date(div):
    """This function extracts the date when the job was posted from the results page.
    
    """
    try:
        spans = div.findAll('span', attrs={'class': 'date'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

def extract_fulltext(url):
    """This function opens the link to the full job description and extracts the job description text.
    
    """
    try:
        page = requests.get('https://de.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': 'jobsearch-jobDescriptionText'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

def extract_location2(url):
    """This function opens the link to the full job description and extracts the job location (since the job location is not always mentioned in the results page).
    
    """
    try:
        page = requests.get('https://de.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('span', attrs={'class': 'jobsearch-JobMetadataHeader-iconLabel'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'
```

## 2. Data Cleaning

#### 2.1. How to run this script

You can find the code [here](https://github.com/Andrea-Giuliani/Python-Project/blob/master/Data_Cleaning/Data_Cleaning.py)

#### 2.2. What the script does?

Data cleaning is the second step of our project. This module prepares the recolected data for analysis. Data almost never comes in clean, especially when doing web scraping. This script merges the two csv files obtained from the previous step. The script treats missing values, shapes the data frame, transforms the types of variables, and visualize the summary statistics of numerical variables.   

With a clean data frame, the script checks for duplicates and generates the main features of the job offers posted in De.Indeed.com in Berlin. Thus, we analized the main information of the job offers extracted, like companies that posted more job offers and types of positions offered for data scientists and analysts. The script plots these results. 

Finally, this module cleans and process the description of the job postings (text column). The script extracts the basic features of text data, does the basic pre-processing of the text, and finally, plots the most frequent words in the text. Therefore, we can identify the main characteristics of job offers and required skills in the job market in Berlin. 

```python
def mark_nan_values(df_merged):
    '''
    We want to mark 'NOT_FOUND' as missing value or NaN. 
    All missing values (before strings) will be interpreted as NaN by Python.
    '''
    df_merged[['Company_name', 'Location','Rating','Job_description','Location2']] = df_merged[['Company_name', 'Location', 'Rating','Job_description', 'Location2']].replace({'NOT_FOUND': np.NaN}) # columns without information in some cells 
    return df_merged


def drop_col(df_merged):
    '''
    We drop the column 'Location' since it has many missing values: drop 'Location'
    '''
    df_merged_drop = df_merged.drop(['Location'], axis=1)
    return df_merged_drop


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


def lemmatization(eng_data_clean_text):
    '''
    We do lemmatization to group together words which do not have the same root. 
    That way they are processed as one item.
    '''
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    return lemmatization()


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
```

## 3.Data Mining

#### 3.1. How to run this script

You can find the code [here](Data_Mining/Andrea_Code_Data_Mining.py)

#### 3.2. What the script does?

This module generates a new column for the indicator variable that reports whether the job posting is in English or German. Furthermore, the script also creates indicator variables for analyzing which programming languages are required in the different job postings. 

```python
def detect_lang(x):
    """This function detects languages in a string creating a new column in the dataframe.
    """
    translate = nlp(str(x)[:200])._.language
    return (translate['language'],translate['score'])


def python(series):
    """This function allows to set set up an ifelse statement to recode the new column named python.
    """
    if series == -1:
        return 0
    else:
        return 1

def remove_nones_return_list(a):
    """This function removes the job ads in the dataframe that do not contain any of the skills that we identified
    """
    c = set(a.split(','))
    try:
        c.remove('None')
    except:
        pass
    return ','.join(list(c))    
```

## 4. Demo

The demo is the fourth and last part of our project. Its main function is to collect the user's inputs regarding his/her programming language skills and then recommend a list of jobs, which better matches these skills. Besides the input related to programming skills, the service also collects user's preferences regarding the language of the job ad (german or english) as well as for how long the job ad has been posted.

The demo was created using [streamlit](https://www.streamlit.io/), which is an open-source Python library that makes it much easier to build customized interfaces. However, to be able to run the code and see our demo, it is important to comply with some requirements.

#### 4.1 How to get started with Streamlit

#### Requisites before using Streamlit 

According to this [link](https://docs.streamlit.io/getting_started.html#prerequisites), before using Streamlit, some prerequisites must be completed:

1. Make sure you have pip (python package manager) installed. See [link](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation#pip-install) for instructions on installing pip.

2. Install Streamlit & Pandas
For this, open the command line and type the following: 

```python
pip install streamlit
pip install pandas
```

#### Instructions for starting the demo 

1. Create a new folder (job_ads). Download the file app.py in this [link](https://github.com/Andrea-Giuliani/Python-Project/blob/master/demo/app.py) containing the Streamlit code.
After this step you should have the file app.py inside the folder job_ads.

2. Navigate to the job_ads folder using the command line. My example below:

```cmd
cd C:\Users\aline\OneDrive\Desktop\Hertie\Hertie School 4th Sem\Phyton\Final Project\job-ads
```

3. Run Streamlit on the command line: 

```cmd
streamlit run app.py 
```

It should produce an output as shown below:
```cmd
" You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.147:8501"
```

4. Open the browser on the displayed URL in the command line and see the dashboard. 

#### Understanding how the code works and seeing the changes live in the demo

At this point, you can only see a working dashboard. If you want also to check or adjust the code and see the changes live,  you can easily modify the code in your IDE, save it, and refresh the browser. 
For that I used Visual Studio Code as IDE, since apparently Streamlit cannot be executed inside Colab .

#### 4.2 How to deploy Streamlit

To deploy our demo we followed strictily this [link](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku), which explain how to deploy one Streamlit dashboard with Heroku ([link](https://job-ads-demo.herokuapp.com/) to Streamlit app).

#### 4.3 What the script does?

You can find the code [here](https://github.com/Andrea-Giuliani/Python-Project/blob/master/demo/app.py) 

This module was divided into three main parts.
- 1st: To create the interface which collects the inputs from the user, using the Streamlit library 
- 2nd: To filter and sort the dataset according to 3 user's inputs - programming language skills, language and date posted.
- 3rd: To display the list with the recommended jobs

The most of the code was based on the official streamlit tutorial, what can be found on this [link](https://docs.streamlit.io/tutorial/create_a_data_explorer_app.html#filter-results-with-a-slider) and it is already well documented.

The only new function created by the group was the funcion calculate_skill_index, as shown here:

```python
def calculate_skill_index(job_ads_row):
    """
    This function calculates the skill fulfillment index, i.e, the percentage of programming skills required by the job ad, which 
    are fulfilled by the user. This function will be applied later for every row in the column skill_clean. Therefore, the argument         needs to be job_ads_row.
    """
    set_skill_row = set(job_ads_row.split(',')) 
    set_user = set(skill_user)
    # Define the match between the two sets: the user and the job_ad
    set_match = set_skill_row.intersection(set_user)
    # Count the lenght of the set_match
    number_skills_match = len(set_match)
    # Count the lenght of the set_ad
    number_skills_ad = len(set_skill_row)
    # Calculate the skills fullfilment percentage for each row
    percentage_index = number_skills_match/number_skills_ad
    return percentage_index
```
