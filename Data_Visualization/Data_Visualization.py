# -*- coding: utf-8 -*-

import pandas as pd

#Import Dataset
df2 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/final_dataset.csv')

#Create Barplot
print("This is the frequency for Python", df2["python"].value_counts())
print("This is the frequency for R", df2[" r"].value_counts())
print("This is the frequency for Java", df2["java"].value_counts())
print("This is the frequency for sas", df2["sas"].value_counts())
print("This is the frequency for SQL", df2["sql"].value_counts())
print("This is the frequency for Stata", df2["stata"].value_counts())
print("This is the frequency for SPSS", df2["spss"].value_counts())
print("This is the frequency for Ruby", df2["ruby"].value_counts())
print("This is the frequency for JavaScript", df2["javascript"].value_counts())
print("This is the frequency for PHP", df2["php"].value_counts())

Requested = [990, 1776, 402, 77, 945, 1, 23, 3, 135, 4]
Not_Requested = [801, 15, 1389, 1714, 846, 1790, 1768, 1788, 1656, 1787]
index = ['Python', 'R', 'Java', 'SAS', 'SQL', 'Stata', 'SPSS', 'Ruby', 'JScript', 'PHP']
df2 = pd.DataFrame({'Requested': Requested,

                   'Not_Requested': Not_Requested}, index=index)

ax = df2.plot.bar(rot=0)
