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

# button to redirect user to voter turnout page
if st.button('Visualize voter turnout data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Voter_Turnout.py')

# button to redirect user to voter opinion by demographic page
if st.button('View voter opinion by demographic', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Demographics.py')

# button to redirect user to voting center page
if st.button('View voting centers near you',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/17_Voting_Center.py')

# button to redirect user to voter info page
if st.button("Complete your voter information survey",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Voter_Survey.py')

# button to redirect user to candidate policies page
if st.button("Get to know a candidate's policies",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Candidate_Policies.py')

# button to redirect user to feedback page
if st.button("Give PollPal some feedback!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_Site_Survey.py')

# button to redirect user to Quiz page
if st.button("Take a quiz to find which political party you most align with",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/16_Predict_Party.py')


