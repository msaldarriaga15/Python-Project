# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:45:33 2020

@author: Andrea
"""

import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

#Import dataset 
df = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/data_clean.csv')

#Create New Column
def detect_lang(x):
    """This function detects languages in a string creating a new column in the dataframe.

    """
    translate = nlp(str(x)[:200])._.language
    return (translate['language'],translate['score'])

df['language'] = df['Job_description'].apply(lambda x: nlp(str(x)[:200])._.language['language'])

#Check the new column
df.head()

#Generate Histogram
df['language'].value_counts().plot(kind='bar')

#Changing names of the Language column with a dictionary to make it more appealing in the demo
cleanup_nums = {"language":{'en': "English", 'de': 'German'}}
df.replace(cleanup_nums, inplace=True)

#Make string Job_description lowercase
df["Job_description"] = df["Job_description"].str.lower()

# Substring to be searched Python
python ='python'
  
# Creating and passing series to new column 
df["python"]= df["Job_description"].str.find(python) 

# Recoding with 1 & 0
def python(series):
    """This function allows to set set up an ifelse statement to recode the new column named python.

    """
    if series == -1:
        return 0
    else:
        return 1

df['python'] = df['python'].apply(python)
df['python'].value_counts()

# Substring to be searched R
r =' r'

# Creating and passing series to new column 
df[" r"]= df["Job_description"].str.find(r) 
  
# Recoding with 1 & 0
def r(series):
    """This function allows to set set up an ifelse statement to recode the new column named r.

    """
    if series == -1:
        return 0
    else:
        return 1

df[' r'] = df[' r'].apply(r)
df[' r'].value_counts()

# Substring to be searched Java
java ='java'
  
# Creating and passing series to new column 
df["java"]= df["Job_description"].str.find(java) 
  
# Recoding with 1 & 0
def java(series):
    """This function allows to set set up an ifelse statement to recode the new column named java.

    """
    if series == -1:
        return 0
    else:
        return 1

df['java'] = df['java'].apply(java)
df['java'].value_counts()

# Substring to be searched C
sas = "sas"
  
# Creating and passing series to new column 
df["sas"]= df["Job_description"].str.find(sas) 
  
# Recoding with 1 & 0
def sas(series):
    """This function allows to set set up an ifelse statement to recode the new column named sas.

    """
    if series == -1:
        return 0
    else:
        return 1

df['sas'] = df['sas'].apply(sas)
df['sas'].value_counts()

# Substring to be searched SQL
sql ='sql'

# Creating and passing series to new column 
df["sql"]= df["Job_description"].str.find(sql) 

# Recoding with 1 & 0
def sql(series):
    """This function allows to set set up an ifelse statement to recode the new column named sql.

    """
    if series == -1:
        return 0
    else:
        return 1

df['sql'] = df['sql'].apply(sql)
df['sql'].value_counts()

# Substring to be searched Stata
stata ='stata'
  
# Creating and passing series to new column 
df["stata"]= df["Job_description"].str.find(stata) 

# Recoding with 1 & 0
def stata(series):
    """This function allows to set set up an ifelse statement to recode the new column named stata.

    """
    if series == -1:
        return 0
    else:
        return 1

df['stata'] = df['stata'].apply(stata)
df['stata'].value_counts()

# Substring to be searched SPSS
spss ='spss'
  
# Creating and passing series to new column 
df["spss"]= df["Job_description"].str.find(spss) 

# Recoding with 1 & 0
def spss(series):
    """This function allows to set set up an ifelse statement to recode the new column named spss.

    """
    if series == -1:
        return 0
    else:
        return 1

df['spss'] = df['spss'].apply(spss)
df['spss'].value_counts()

# Substring to be searched Ruby
ruby ='ruby'
  
# Creating and passsing series to new column 
df["ruby"]= df["Job_description"].str.find(ruby) 

# Recoding with 1 & 0
def ruby(series):
    """This function allows to set set up an ifelse statement to recode the new column named ruby.

    """
    if series == -1:
        return 0
    else:
        return 1
    
df['ruby'] = df['ruby'].apply(ruby)
df['ruby'].value_counts()

# Substring to be searched JavaScript
javascript ='javascript'
  
# Creating and passsing series to new column 
df["javascript"]= df["Job_description"].str.find(javascript) 

# Recoding with 1 & 0
def javascript(series):
    """This function allows to set set up an ifelse statement to recode the new column named javascript.

    """
    if series == -1:
        return 0
    else:
        return 1

df['javascript'] = df['javascript'].apply(javascript)
df['javascript'].value_counts()

# Substring to be searched PHP
php ='php'
  
# Creating and passsing series to new column 
df["php"]= df["Job_description"].str.find(php) 

# Recoding with 1 & 0
def php(series):
    """This function allows to set set up an ifelse statement to recode the new column named php.

    """
    if series == -1:
        return 0
    else:
        return 1

df['php'] = df['php'].apply(php)
df['php'].value_counts()

# Transforming the categorical variables / 10 Skills columns into a list - this is a preprocessing necessary for the demo

# First, turning 0,1 to names with a dictionary
cleanup_nums = {"python":{1: "python", 0: None},
                " r": {1: " r", 0: None}, "java": {1: "java", 0: None},
                "sas": {1: "sas", 0: None}, "sql": {1: "sql", 0: None}, "stata": {1: "stata", 0: None}, 
                "spss": {1: "spss", 0: None}, "ruby": {1: "ruby", 0: None}, "javascript": {1: "javascript", 0: None},
                "php": {1: "php", 0: None}}
df.replace(cleanup_nums, inplace=True)


# Concatenate the columns into a new column named skills_as_list
# df_combined = ",".join()df['Python'].map(str) + ',' + df['Ruby'].map(str)
cols_list = ['python', " r", "java", "sas", "sql", "stata", "spss", "ruby", "javascript", "php"]
df['skills_as_list'] = df.apply(lambda x: ','.join([str(x[col_name]) for col_name in cols_list]),
                                axis=1)

#Remove job_ads where no skill was found. There were 4 lines like this. And this is also important for the demo to work.
def remove_nones_return_list(a):
    """This function removes the job ads in the dataframe that do not contain any of the skills that we identified

    """
    c = set(a.split(','))
    try:
        c.remove('None')
    except:
        pass
    return ','.join(list(c))
df['skill_clean'] = df['skills_as_list'].apply(remove_nones_return_list)

#Export df to be used by streamlit
df.to_csv(r'C:\Users\K501UX\Desktop\Hertie School\Fourth Semester\Python\Python Project\final_dataset.csv', index=False)