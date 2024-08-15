import logging
logger = logging.getLogger(__name__)

import streamlit as st
# TODO: implement SideBarLinks
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

response = requests.get('http://api:4000/v/voter-id')

if response.status_code == 200:
    voter_ids_dict = response.json() 
    voterIds = sorted([item['voterId'] for item in voter_ids_dict])
else:
    st.error(f"Failed to retrieve voter IDs. Status code: {response.status_code}")
    voterIds = []

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Site Feedback')

with st.form(key='feedback_form'):
  voterId = st.selectbox("Select Voter ID", voterIds)
  foundVotingCenter = st.radio("Did you find a voting center through PollPal?", ('Yes', 'No'))
  howUserFriendly = st.slider("On a scale of 1-10, how user friendly was PollPal?", min_value=1, max_value=10, step=1)
  isDataUseful = st.slider("On a scale of 1-10, how much of the info we provided met your needs?",  min_value=1, max_value=10, step=1)
  informedAboutCandidate = st.radio("Do you feel informed about the candidates?", ('Yes', 'No'))
  discoveredWhere = st.text_area("How did you discover us?")
  submitted = st.form_submit_button("Submit")

if submitted:
  data = {}
  data['voterId'] = voterId
  data['foundVotingCenter'] = foundVotingCenter
  data['isUserFriendly'] = howUserFriendly
  data['foundNeededInfo'] = isDataUseful
  data['informedAboutCandidate'] = informedAboutCandidate
  data['discoveredWhere'] = discoveredWhere
  
  requests.post('http://api:4000/v/voter-site-survey', json=data)
  if response.status_code == 200:
    st.success('Voter Feedback survey response submitted!')
  else:
    st.error(f"Failed to submit survey. Status code: {response.status_code}")