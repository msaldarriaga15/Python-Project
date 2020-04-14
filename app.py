import streamlit as st
import pandas as pd

### 1st task ### >> Create an user interface with a dropdown menu for collecting user's interface

#Load the excel file and read it as a table. We used a mockdataset with only 100 entries at this point.
def load_data():
    df = pd.read_csv('mock_dataset.csv',sep=',') 
    return df

df = load_data()

# Create a dropdown menu, which reads the Column "Language" in the dataset and provides the possible values 
# for the user. # We are using here "selectbox" assuming that the user can only click on one of the languages - german or 
# english.
language_user = st.sidebar.selectbox("1. Select your preferred language: ", df['Language'].unique())

# Regarding the skills, we still do not have in the database a column with all the skills required by each job
# ads. Therefore, we basically created manually a list with 10 skills, named "hardcoded_skills"
# We are using "multiselect" rather than "selectbox" assuming that the user want to select more than one skills .
hardcoded_skills = ['Machine Learning','Data Mining','Python','R','SQL','Java','Django','C','Oracle','ETL']
skills = st.sidebar.multiselect("2. Select your skills:", hardcoded_skills)

### 2nd task ## >> Display a recommendation list

#Filter the dataset by "Language"
filtered_df = df[df["Language"] == language_user]

#Create a header in the page
st.header('Here is the list of your best matching job ads TEST')

#Change the format and the design of the list. # ** to turn it bold
for job_index, line in enumerate(filtered_df.itertuples()):
    st.markdown('### {}. {} at {} ' .format(job_index + 1, line.job_title, line.company_name)) 
    st.markdown('**Skills:** {}'.format(line.Skills))
    st.markdown('Click [here]({}) to apply'.format(line.link))

