import logging
import requests
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks


SideBarLinks()

st.write("# Voter Demographic Survey")

response = requests.get('http://api:4000/v/candidate-names')
if response.status_code == 200:
    candidate_info = response.json()
    candidate_names = sorted([str(item['candidateId']) + " " +item['firstName'] + " " + item['lastName'] for item in candidate_info])
else:
    st.error(f"Failed to retrieve candidate info. Status code: {response.status_code}")
    candidate_names = []


state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

with st.form(key='feedback_form'):
  politicalAffiliaton = st.selectbox("Which party do you affiliate with?", ('Democrat', 'Republican', 'Independent'))
  state = st.selectbox("Which state are you a resident of?", state_names)
  county = st.text_input("Which county do you reside in?")
  age = st.text_input("How old are you?")
  incomeLevel = st.selectbox("What is your approximate income level?", ('0-$30,000', '$30,000-$58,000', '$58,000-$94,000', '$94,000-$153,000', '> $153,000'))
  ethnicity = st.selectbox("Which ethnicity do you identifiy by?", ('Native American or Alaska Native', 'Asian', 'Black or African American', 'Native Hawaiian or Other Pacific Islander', 'White', 'Hispanic or Latino'))
  gender= st.selectbox("Which gender do you identify by?", ('Male', 'Female', 'Other'))
  candidateId = st.radio("Who are you voting for?", candidate_names)
  submitted = st.form_submit_button("Submit")

if submitted:
  data = {}
  data['politicalAffiliation'] = politicalAffiliaton
  data['state'] = state
  data['county'] = county
  data['age'] = age
  data['incomeLevel'] = incomeLevel
  data['ethnicity'] = ethnicity
  data['gender'] = gender
  data['candidateId'] = candidateId.split(" ")[0]
  st.write(data)
  
  requests.post(f'http://api:4000/v/voter-info', json=data)
