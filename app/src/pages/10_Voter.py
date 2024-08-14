import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome voter, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Visualize voter turnout data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Voter_Turnout.py')

if st.button('View voter opinion by demographic', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Demographics.py')

if st.button('View voting centers near you',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/17_Voting_Center.py')

if st.button("Complete your voter information survey",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Voter_Survey.py')

if st.button("Get to know a candidate's policies",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Candidate_Policies.py')

if st.button("Give PollPal some feedback!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_Site_Survey.py')

if st.button("Take a quiz to find your political party",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/16_Predict_Party.py')


