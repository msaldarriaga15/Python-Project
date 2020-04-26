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

You can find the code [here](include link)

#### 2.2. What the script does?

Mari write here... and copy his functions..

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

## 4. Construction of the Demo

The demo is the fourth and last part of our project. Its main function is to collect the user's inputs regarding his/her programming language skills and then recommend a list of jobs, which better matches these skills. Besides the input related to programming skills, the service also collects user's preferences regarding the language of the job ad (german or english) as well as for how long the job ad has been posted.

The demo was created using streamlit, which is an open-source Python library that makes it much easier to build customized interfaces. However, to be able to run the code and see our demo, it is important to comply with some requirements.

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

cd C:\Users\aline\OneDrive\Desktop\Hertie\Hertie School 4th Sem\Phyton\Final Project\job-ads

3. Run Streamlit on the command line: streamlit run app.py 
It should produce an output as shown below:

" You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.147:8501"
  
4. Open the browser on the displayed URL in the command line and see the dashboard. 

#### Understanding how the code works and seeing the changes live in the demo

At this point, you can only see a working dashboard. If you want also to check or adjust the code and see the changes live,  you can easily modify the code in your IDE, save it, and refresh the browser. 
For that I used Visual Studio Code as IDE, since apparently Streamlit cannot be executed inside Colab .

#### 4.2 How to deploy Streamlit

To deploy our demo we followed strictily this [link](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku), which explain how to deploy one Streamlit dashboard with Heroku.

#### 4.3 What the script does?

You can find the code [here](https://github.com/Andrea-Giuliani/Python-Project/blob/master/demo/app.py) 

This module was divided into three main parts.
- 1st: To create the interface which collects the inputs from the user, using streamlit library 
- 2nd: To filter ans sort the dataset according to 3 user's inputs - programming language skills, language and date posted.
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
