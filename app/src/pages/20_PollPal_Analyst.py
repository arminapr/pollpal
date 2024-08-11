import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome PollPal Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Delete Invalid User Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_delete_invalid_data.py')

if st.button('View Voter Data By Demographic',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_voter_demographics.py')

if st.button("View User Site Surveys",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_user_site_survey.py')