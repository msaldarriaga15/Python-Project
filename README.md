# Python-Project
Project for the class "GRAD-E1326: Python Programming for Data Scientists"

This project was divided into 4 main parts and it will be documented accordingly. 

## 1. Web Scraping

#### 1.1. How to run this script

You can find the code [here](include link)

#### 1.2. What the script does?

Toma write here....

## 2. Data_Cleaning

#### 2.1. How to run this script

You can find the code [here](include link)

#### 2.2. What the script does?

Mari write here... and copy his functions..

## 3.Data Mining

#### 3.1. How to run this script

You can find the code [here](Data_Mining/Andrea_Code_Data_Mining.py)

#### 3.2. What the script does?

This module generates a new column for the indicator variable that reports whether the job posting is in English or German. Furthermore, the script also creates indicator variables for analyzing which programming lnaguages are required in the different job postings. 

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
