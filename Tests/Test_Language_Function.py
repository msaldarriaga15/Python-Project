# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:42:07 2020

@author: K501UX
"""
import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import unittest

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

def detect_lang(input_string_to_be_detected):
    """
    This function detects languages in a string creating a new column in the dataframe
    """
    return nlp(str(input_string_to_be_detected)[:200])._.language['language']

class TestStringMethods(unittest.TestCase):

    def test_german(self):
        """ ADD DESCRIPTION """
        german_sentence = "Ich bin ein Berliner und ich liebe Python"
        language_detected = detect_lang(german_sentence)
        self.assertEqual(language_detected, 'de')

    def test_english(self):
        """ ADD DESCRIPTION """
        english_sentence = "I am in Berlin and I love Python"
        language_detected = detect_lang(english_sentence)
        self.assertEqual(language_detected, 'en')