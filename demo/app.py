"""
This section of the code is exclusive for programming our demo, as the third and last part of our project.

The overall function of the demo is to collect the input of the user regarding his/her programming language skills and 
then recommend a list of jobs, which better match these skills Besides the input related to skills, the demo
also uses the langauge of the job ad (german or english) as well as how long the job ad has been posted 
to filter and sort this job list.

The demo was created using streamlit, which is an open-source Python library that makes it easy to build beautiful
custom web-apps data science. Later on, the demo was deployed with the use Heroku.

All the requirements to run the demo locally as well as to deploy it are detialed in the file Read.me
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

def load_data():
    """
    This function loads the excel file and read it as a table. The file used is the output from our data mining phase. 
    """
    csv_filepath = os.path.abspath(__file__ + "/../../data/final_dataset.csv")
    df = pd.read_csv(csv_filepath,sep=',') 
    return df

df = load_data()

# First part - Create the interface which will collect the inputs from the user.
# As already mentioned, streamlit allows to create all these widgets with few lines of codes.

# Function: Create a slider widget - from min. 1 to max. 30 days and place it in a sidebar 
days_to_filter = st.sidebar.slider('1. Filter jobs by date posted: (1-30 days ago)', 1, 30) # min: 1 days, max =30

# Function: Create a dropdown menu, which reads the Column "Language" in the dataset and provides the uniques values found on it.
# We are using here "selectbox" assuming that the user can only click on one of the languages - either german or 
# english.
language_user = st.sidebar.selectbox("2. Select your preferred language: ", df['language'].unique())

# Function:  Create a dropdown menu for programming languages and place it in a sidebar.
# In this case we used multiselect, given that the user can select more than one programming skill
# Besides, we also created manually a list of skills with the 10 programming languages, which were used in the 
# mining phase. 
list_skills = ['php','javascript','python',' r','sql','java','stata','sas','ruby','spss']# based on the most useful skills in the market - Andrea article
skill_user = st.sidebar.multiselect("3. Select the programming language(s) you know: ",list_skills)

# Second part - To display a recommendation list, which is filtered and sorted according to the inputs from the users

#Function: Filter the dataset by the "Language" selected in the dropdown menu
filtered_df = df[df["language"] == language_user]

#Function: Filter the dataset by the "Date posted" selected in the slider
filtered_df = filtered_df[filtered_df["Days_posted_2"] <= days_to_filter]

# New function to create skill fullfilment per row. Idea here is that for each 

def calculate_skill_index(row):
     """
    This function calculates the skill_fullfilment index, i.e, the percentage of programming skills required by the ad, which are fulfilled by the user
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

# we filter out jobs that do not require any skills
filtered_df = filtered_df[~filtered_df['skill_clean'].isna()]

#Filtering jobs by skills and lists
filtered_df['fullfilment_index']= filtered_df["skill_clean"].apply(calculate_skill_index)

filtered_df.sort_values(by=['fullfilment_index','Days_posted_2'], ascending=[False,True], inplace=True)


#Create a header in the page
st.header('Here is the list of your best matching job ads:')

#Change the format and the design of the list. # ** to turn it bold
for job_index, line in enumerate(filtered_df[:20].itertuples()):
    st.markdown('### {}. {} at {} ' .format(job_index + 1, line.Job_title, line.Company_name)) 
    st.markdown('- You comply with **{:.1f}%** of the skills'.format(line.fullfilment_index*100))
    st.markdown('- Programming skills required: {}' .format(line.skill_clean))
    st.markdown('- Description: {} ...'.format(line.Job_description[:150]))
    st.markdown('- Click [here]({}) to see the full description and to apply'.format(line.Website))
    st.markdown('- This position has been posted in the last: **{:.0f} days**'.format(line.Days_posted_2))
    st.markdown('------------------------')
