"""add description"""

import streamlit as st
import pandas as pd
import numpy as np

### 1st task ### >> Create an user interface with a dropdown menu for collecting user's interface

#Load the excel file and read it as a table. We used a mockdataset with only 100 entries at this point.
def load_data():
    df = pd.read_csv('final_dataset.csv',sep=',') 
    return df

df = load_data()


#Create dropdrown menu for days
days_to_filter = st.sidebar.slider('1. Filter jobs by date posted: (1-30 days ago)', 1, 30)  # min: 1 days, max =30

# Create a dropdown menu, which reads the Column "Language" in the dataset and provides the possible values 
# for the user. # We are using here "selectbox" assuming that the user can only click on one of the languages - german or 
# english.

language_user = st.sidebar.selectbox("2. Select your preferred language: ", df['language'].unique())

### 2nd task ## >> Display a recommendation list

#Filter the dataset by "Language"
filtered_df = df[df["language"] == language_user]


#Create dropdown menu for skills
list_skills = ['php','javascript','python',' r','sql','java','stata','sas','ruby','spss']# based on the most useful skills in the market - Andrea article
skill_user = st.sidebar.multiselect("3. Select your Skills: ",list_skills)

#Create new function to create skill fullfilment per row

def calculate_skill_index(row):
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

# we filter out jobs that do not require any skills
filtered_df = filtered_df[~filtered_df['skill_clean'].isna()]

#Filtering jobs by skills and lists
filtered_df['fullfilment_index']= filtered_df["skill_clean"].apply(calculate_skill_index)
filtered_df = filtered_df[filtered_df["Days_posted_2"] <= days_to_filter]
filtered_df.sort_values(by=['fullfilment_index','Days_posted_2'], ascending=[False,True], inplace=True)


#Create a header in the page
st.header('Here is the list of your best matching job ads:')

#Change the format and the design of the list. # ** to turn it bold
for job_index, line in enumerate(filtered_df[:20].itertuples()):
    st.markdown('### {}. {} at {} ' .format(job_index + 1, line.Job_title, line.Company_name)) 
    st.markdown('You comply with **{:.1f}%** of the skills'.format(line.fullfilment_index*100))
    st.markdown('Skills required: {}' .format(line.skill_clean))
    st.markdown('Click [here]({}) to apply'.format(line.Website))
    st.markdown('This position has been posted for: **{} days**'.format(line.Days_posted_2))
    st.markdown('------------------------')
