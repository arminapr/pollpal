import logging
logger = logging.getLogger(__name__)

import streamlit as st
# TODO: implement SideBarLinks
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Site Feedback')

with st.form(key='feedback_form'):
  foundVotingCenter = st.radio("Did you find a voting center?", ('True', 'False'))
  howUserFriendly = st.slider("On a scale of 1-10, how user friendly was the site?", min_value=1, max_value=10, step=1)
  isDataUseful = st.slider("on a scale of 1-10, how much of the info we provided met your needs?",  min_value=1, max_value=10, step=1)
  informedAboutCandidate = st.radio("do you feel informed about the candidates?", ('True', 'False'))
  discoveredWhere = st.text_area("how did you discover us?")
  submitted = st.form_submit_button("Submit")

if submitted:
  data = {}
  data['foundVotingCenter'] = foundVotingCenter
  data['isUserFriendly'] = howUserFriendly
  data['foundNeededInfo'] = isDataUseful
  data['informedAboutCandidate'] = informedAboutCandidate
  data['discoveredWhere'] = discoveredWhere
  st.write(data)
  
  requests.post(f'http://api:4000/v/voter-site-survey/', json=data)