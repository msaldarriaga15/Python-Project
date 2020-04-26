# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import unittest as ut
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob, Word
nltk.download('stopwords')
stop = stopwords.words('english')


# unittests for the web scraping
# Testing whether the link provided returns the desired list of results


class TestDataAnalyst(unittest.TestCase):    
    bsObj = None    
    def setUpClass():        
        global bsObj        
        url = "https://de.indeed.com/Jobs?q=data+analyst&l=Berlin"        
        bsObj = BeautifulSoup(urlopen(url))    
        
    def test_titleText(self):        
        global bsObj        
        pageTitle = bsObj.find("h1").get_text()        
        self.assertEqual("\n            data analyst Jobs - Berlin", pageTitle);    
        
                
if __name__ == '__main__':    
     unittest.main()
     

class TestDataScientist(unittest.TestCase):    
    bsObj = None    
    def setUpClass():        
        global bsObj        
        url = "https://de.indeed.com/Jobs?q=data+scientist&l=Berlin"        
        bsObj = BeautifulSoup(urlopen(url))    
        
    def test_titleText(self):        
        global bsObj        
        pageTitle = bsObj.find("h1").get_text()        
        self.assertEqual("\n            data scientist Jobs - Berlin", pageTitle);    
        
                
if __name__ == '__main__':    
     unittest.main()
     
# Tests for the data cleaning
# Read the file into a dataFrame
df1 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/jobs_data+analyst.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/jobs_data+scientist.csv')

# Merge two datasets
df_merged = df1.append(df2, ignore_index=True)

# Test for missing values
def mark_nan_values(df_merged):
    '''
    We want to mark 'NOT_FOUND' as missing value or NaN. 
    All missing values (before strings) will be interpreted as NaN by Python.
    '''
    df_merged[['Company_name', 'Location','Rating','Job_description','Location2']] = df_merged[['Company_name', 'Location', 'Rating','Job_description', 'Location2']].replace({'NOT_FOUND': np.NaN}) # columns without information in some cells 
    return df_merged


class TestNaN(unittest.TestCase):

    def test_NaN(self):
        '''
        Test the NaN
        '''
        rating = [1, 2, 3, 'NOT_FOUND', 4, 'NOT_FOUND', 6]
        non_missing_values = [1, 2, 3, 31, 4, 5, 6]
        df = pd.DataFrame({'Rating':rating,'Company_name':non_missing_values, 'Location':non_missing_values,'Job_description':non_missing_values, 'Location2':non_missing_values})
        #index = 1
        rating_NaN = mark_nan_values(df)
        pd.testing.assert_series_equal(pd.Series([1, 2, 3, np.NaN, 4, np.NaN, 6]), rating_NaN['Rating'], check_names=False)
        
# Test to drop columns    
def drop_col(df_merged):
    '''
    We drop the column 'Location' since it has many missing values: drop 'Location'
    '''
    df_merged_drop = df_merged.drop(['Location'], axis=1)
    return df_merged_drop

class TestDrop(unittest.TestCase):

    def test_drop(self):
        '''
        We want to test if our function is dropping the column Location. 
        '''

        df = pd.DataFrame(columns=['Rating','Location','City']) 
        df_drop_expected = pd.DataFrame(columns=['Rating','City'])
        
        df_drop = drop_col(df)
        pd.testing.assert_frame_equal(df_drop, df_drop_expected)

# Test for duplicate rows 
def check_duplicates(data_clean):
    '''
    This function is to find duplicate rows. 
    ''' 
    duplicate_rowsdf = data_clean[data_clean.duplicated(keep=False)]
    return duplicate_rowsdf

class TestRemoveDuplicates(unittest.TestCase):
    '''
    Test for function remove_duplicates
    '''
    def test_general_case(self):
        '''
        Test remove_shared where there are items that
        appear in both lists, and items that appear in
        only one or the other list.
        '''
        df = pd.DataFrame([1,2,3,4,1],columns=['a'])
        df_expected = pd.DataFrame([1,1],columns=['a'])
        df_only_duplicates = check_duplicates(df).reset_index(drop=True) # We need to reset the index because otherwise row indices do not match
        pd.testing.assert_frame_equal(df_only_duplicates, df_expected)
        

# Test for test processing
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
    eng_data_clean_text['Job_description'] = eng_data_clean_text['Job_description'].apply(lambda x: str(TextBlob(x).correct())) # Spelling correction
    return eng_data_clean_text


class TestProcessing (unittest.TestCase):

    def test_processing(self):
        '''
        Test we process lower strings, remove punctuation, remove stopwords,
        and spelling correction.
        '''
        pre_process = "For Data sciEntits. is important worK team"
        df = pd.DataFrame([pre_process],columns=['Job_description'])
        post_process = basic_pre_processing(df)
        first_value = post_process['Job_description'][0]
        self.assertEqual(first_value, 'data scientist important work team')
        

if __name__ == '__main__':
    unittest.main(exit=False)

# Test for data mining 
# Define the spacy_langdetect function
nlp = spacy.load("en_core_web_sm")

def detect_lang(input_string_to_be_detected):
    """
    This function detects languages in a string creating a new column in the dataframe
    """
    return nlp(str(input_string_to_be_detected)[:200])._.language['language']

class TestStringMethods(unittest.TestCase):

    def test_german(self):
        """ This function detects whether the string is written in German """
        german_sentence = "Ich bin ein Berliner und ich liebe Python"
        language_detected = detect_lang(german_sentence)
        self.assertEqual(language_detected, 'de')

    def test_english(self):
        """ This function detects whether the string is written in English """
        english_sentence = "I am in Berlin and I love Python"
        language_detected = detect_lang(english_sentence)
        self.assertEqual(language_detected, 'en')

# Test for the demo
def calculate_skill_index(row,skill_user):
    """
    This function calculates the skill_fullfilment index, i.e, the percentage of 
    programming skills required by the job ad, which are fulfilled by the user
    """
    set_row = set(row.split(','))
    set_user = set(skill_user)
    set_match = set_row.intersection(set_user)
    #count the lenght of the set_match
    number_skills_match = len(set_match)
    #count the lenght of the set_ad
    number_skills_ad = len(set_row)
    #create the skills fullfilment, i.e, skills_match divided by skills_ads
    percentage_index = number_skills_match/number_skills_ad
    return percentage_index

class TestStringMethods(ut.TestCase):

    def test_skill_index(self):
        """ This test checks whether the function calculate_skill_index calculates 
        the right skill fulfillment percentage """
        set_row = "python,sql,r,stata"
        skill_user = ["python","java","javascript"]
        self.assertEqual(calculate_skill_index(set_row,skill_user), 0.25)

if __name__=='__main__':
    ut.main(argv=[''],exit=False)
