# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:42:07 2020

@author: K501UX
"""

# unittests for the web scraping
# Testing whether the link provided returns the desired list of results

from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import unittest as ut

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

#Define the spacy_langdetect function
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