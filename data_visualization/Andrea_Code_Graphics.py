# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:29:45 2020

@author: Andrea
"""
import pandas as pd

#Import Dataset
df2 = pd.read_csv('https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/data_indicator_variables.csv')

#Create Barplot
print("This is the frequency for Python", df2["Python"].value_counts())
print("This is the frequency for R", df2["R"].value_counts())
print("This is the frequency for Java", df2["Java"].value_counts())
print("This is the frequency for C", df2["C"].value_counts())
print("This is the frequency for SQL", df2["SQL"].value_counts())
print("This is the frequency for Stata", df2["Stata"].value_counts())
print("This is the frequency for SPSS", df2["SPSS"].value_counts())
print("This is the frequency for Ruby", df2["Ruby"].value_counts())
print("This is the frequency for JavaScript", df2["JavaScript"].value_counts())
print("This is the frequency for PHP", df2["PHP"].value_counts())

Requested = [982, 1698, 402, 1739, 945, 1, 23, 3, 25, 4]
Not_Requested = [809, 93, 1389, 52, 846, 1790, 1768, 1788, 176, 1787]
index = ['Python', 'R', 'Java', 'C', 'SQL', 'Stata', 'SPSS', 'Ruby', 'JScript', 'PHP']
df2 = pd.DataFrame({'Requested': Requested,

                   'Not_Requested': Not_Requested}, index=index)

ax = df2.plot.bar(rot=0)