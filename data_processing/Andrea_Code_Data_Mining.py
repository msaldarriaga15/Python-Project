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
df = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/df_cleanv2(merge).csv')

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

# Substring to be searched Python
Python ='Python'
  
# Creating and passing series to new column 
df["Python"]= df["Job_description"].str.find(Python) 

# Recoding with 1 & 0
def Python(series):
    """This function allows to set set up an ifelse statement to recode the new column named Python.

    """
    if series == -1:
        return 0
    else:
        return 1


df['Python'] = df['Python'].apply(Python)
df['Python'].value_counts()

# Substring to be searched R
R =' R'

# Creating and passing series to new column 
df["R"]= df["Job_description"].str.find(R) 
  
# Recoding with 1 & 0
def R(series):
    """This function allows to set set up an ifelse statement to recode the new column named R.

    """
    if series == -1:
        return 0
    else:
        return 1

df['R'] = df['R'].apply(R)
df['R'].value_counts()

# Substring to be searched Java
Java ='Java'
  
# Creating and passing series to new column 
df["Java"]= df["Job_description"].str.find(Java) 
  
# Recoding with 1 & 0
def Java(series):
    """This function allows to set set up an ifelse statement to recode the new column named Java.

    """
    if series == -1:
        return 0
    else:
        return 1

df['Java'] = df['Java'].apply(Java)
df['Java'].value_counts()

# Substring to be searched C
C = " C"
  
# Creating and passing series to new column 
df["C"]= df["Job_description"].str.find(C) 
  
# Recoding with 1 & 0
def C(series):
    """This function allows to set set up an ifelse statement to recode the new column named C.

    """
    if series == -1:
        return 0
    else:
        return 1

df['C'] = df['C'].apply(C)
df['C'].value_counts()

# Substring to be searched SQL
SQL ='SQL'

# Creating and passing series to new column 
df["SQL"]= df["Job_description"].str.find(SQL) 

# Recoding with 1 & 0
def SQL(series):
    """This function allows to set set up an ifelse statement to recode the new column named SQL.

    """
    if series == -1:
        return 0
    else:
        return 1

df['SQL'] = df['SQL'].apply(SQL)
df['SQL'].value_counts()

# Substring to be searched Stata
Stata ='Stata'
  
# Creating and passing series to new column 
df["Stata"]= df["Job_description"].str.find(Stata) 

# Recoding with 1 & 0
def Stata(series):
    """This function allows to set set up an ifelse statement to recode the new column named STATA.

    """
    if series == -1:
        return 0
    else:
        return 1

df['Stata'] = df['Stata'].apply(Stata)
df['Stata'].value_counts()

# Substring to be searched SPSS
SPSS ='SPSS'
  
# Creating and passing series to new column 
df["SPSS"]= df["Job_description"].str.find(SPSS) 

# Recoding with 1 & 0
def SPSS(series):
    """This function allows to set set up an ifelse statement to recode the new column named SPSS.

    """
    if series == -1:
        return 0
    else:
        return 1

df['SPSS'] = df['SPSS'].apply(SPSS)
df['SPSS'].value_counts()

# Substring to be searched Ruby
Ruby ='Ruby'
  
# Creating and passsing series to new column 
df["Ruby"]= df["Job_description"].str.find(Ruby) 

# Recoding with 1 & 0
def Ruby(series):
    """This function allows to set set up an ifelse statement to recode the new column named Ruby.

    """
    if series == -1:
        return 0
    else:
        return 1
    
df['Ruby'] = df['Ruby'].apply(Ruby)
df['Ruby'].value_counts()

# Substring to be searched JavaScript
JavaScript ='JavaScript'
  
# Creating and passsing series to new column 
df["JavaScript"]= df["Job_description"].str.find(JavaScript) 

# Recoding with 1 & 0
def JavaScript(series):
    """This function allows to set set up an ifelse statement to recode the new column named JavaScript.

    """
    if series == -1:
        return 0
    else:
        return 1

df['JavaScript'] = df['JavaScript'].apply(JavaScript)
df['JavaScript'].value_counts()

# Substring to be searched PHP
PHP ='PHP'
  
# Creating and passsing series to new column 
df["PHP"]= df["Job_description"].str.find(PHP) 

# Recoding with 1 & 0
def PHP(series):
    """This function allows to set set up an ifelse statement to recode the new column named PHP.

    """
    if series == -1:
        return 0
    else:
        return 1

df['PHP'] = df['PHP'].apply(PHP)
df['PHP'].value_counts()

#Export dataset as CSV
df.to_csv(r'C:\Users\K501UX\Desktop\Hertie School\Fourth Semester\Python\Python Project\data_indicator_variables.csv', index = False)


