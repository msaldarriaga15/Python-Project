"""
This code section is exclusive for creating our demo, as the third and last part of our project.

The overall function of the demo is to collect the user's inputs regarding his/her programming language skills and 
then recommend a list of jobs, which better matches his/her skills.
Besides the input related to programming skillss, the service also collects the preferences of the user regarding the language of the job ads 
(german or english) as well as for how long the job ad has been posted.

The code is divided into three main parts:

1st: To create the interface which collects the inputs from the user, using streamlit library 
2nd: To filter ans sort the dataset according to 3 user's inputs - programming language skills, language and date posted.
3rd: To display the list with the recommended jobs

The demo was created using streamlit, which is an open-source Python library that makes it much easier to build customized interfaces.
Finally, the demo was deployed with the use Heroku.

All the requirements to run the demo locally as well as to deploy it are detailed in the file Read.me
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

def load_data():
    """
    This function loads the excel file final_dataset and read it as a table.  
    """
    df = pd.read_csv("https://raw.githubusercontent.com/Andrea-Giuliani/Python-Project/master/data/final_dataset.csv",sep=',') 
    return df

df = load_data()


#### 1st: To create the interface which collects the inputs from the user, using streamlit library  #### 

# Create a slider widget - from min. 1 to max. 30 days and place it in a sidebar 
days_to_filter = st.sidebar.slider('1. Filter jobs by date posted: (1-30 days ago)', 1, 30) 

# Create a dropdown menu, which reads the Column "Language" in the dataset and provides the uniques values found on it.
# We are using here "selectbox" assuming that the user can only click on one of the languages - either german or english.
language_user = st.sidebar.selectbox("2. Select your preferred language: ", df['language'].unique())

# Create a dropdown menu with the 10 programming languages and place it in a sidebar.
# In this case we used multiselect, assuming that the user can select more than one programming skill.
# The list_skills was created with these 10 programming languages, based on the same ones used in the data mining phase. 
list_skills = ['php','javascript','python',' r','sql','java','stata','sas','ruby','spss']
skill_user = st.sidebar.multiselect("3. Select the programming language(s) you know: ",list_skills)



#### 2nd: To filter ans sort the dataset according to 3 user's inputs - programming language skills, language and date posted.####

# Filter the dataset by the "Language" selected in the dropdown menu by the user
filtered_df = df[df["language"] == language_user]

# Filter the dataset by the "Date posted" selected in the slider by the user
filtered_df = filtered_df[filtered_df["Days_posted_2"] <= days_to_filter]

# Create a new function which calculates the skill fulfillment index per row, i.e, the percentage of programming skills 
# required by the job ad, which are fulfilled by the user
def calculate_skill_index(job_ads_row):
    """
    This function calculates the skill fulfillment index, i.e, the percentage of programming skills required by the ad, which 
    are fulfilled by the user. 
    This function will be applied later for every row in the column skill_clean. Therefore, the argument needs to be job_ads_row
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

# Filter out jobs that do not require any skills
filtered_df = filtered_df[~filtered_df['skill_clean'].isna()]

# Create a new column, with this skill fulfillment index
filtered_df['fullfilment_index']= filtered_df["skill_clean"].apply(calculate_skill_index)

# Finally, filter the dataset by the skill index and then by the Date posted
filtered_df.sort_values(by=['fullfilment_index','Days_posted_2'], ascending=[False,True], inplace=True)


#### To display the list with the recommended jobs ####

# Create a header in the page
st.header('Here is the list of your best matching job ads:')

# Modify the format and the design of the list, according to markdown language
for job_index, line in enumerate(filtered_df[:20].itertuples()):
    st.markdown('### {}. {} at {} ' .format(job_index + 1, line.Job_title, line.Company_name)) 
    st.markdown('- You comply with **{:.1f}%** of the skills'.format(line.fullfilment_index*100))
    st.markdown('- Programming skills required: {}' .format(line.skill_clean))
    st.markdown('- Description: {} ...'.format(line.Job_description[:150]))
    st.markdown('- Click [here]({}) to see the full description and to apply'.format(line.Website))
    st.markdown('- This position has been posted in the last: **{:.0f} days**'.format(line.Days_posted_2))
    st.markdown('------------------------')
