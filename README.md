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

## 2. Data_Cleaning

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

## 4. Demo

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

3. Create a new folder (job_ads). Download the CSV file mock_dataset.csv and the file app.py containing the Streamlit code using the links below.
MODIFIYYY!

Just to make sure, I am also sending the files to you attached in the e-mail message.

After this step you should have the files mock_dataset.csv and app.py inside the folder job_ads.

4. Navigate to the job_ads folder using the command line. My example below:

cd C:\Users\aline\OneDrive\Desktop\Hertie\Hertie School 4th Sem\Phyton\Final Project\job-ads

5. Run Streamlit on the command line: streamlit run app.py 
It should produce an output as shown in the image below:
 
6. Open the browser on the displayed URL in the command line and see the dashboard. 

#### Understanding how the code works and seeing the changes live in the demo

- At this point, you can only see a working dashboard. 
- If you want also to check or adjust the code and see the changes live,  you can easily modify the code in your IDE, save it, and refresh the browser, as I did today in our video call. 
- For that I used Visual Studio Code as IDE, since apparently Streamlit cannot be executed inside Colab .

#### 4.2 How to deploy Streamlit

To deploy our demo we followed strictily this [link](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku), which explain how to deploy one Streamlit dashboard with Heroku.

#### 4.3 Code documentation

ALINE WRITE HERE....
