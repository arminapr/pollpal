import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Campaign Manager, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# creating button redirecting manager to view polling data page
if st.button('View Polling Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Polling_Data.py')

# creating button redirecting manager to find swing states page
if st.button('Find Swing States', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Swing_States.py')

# creating button redirecting manager to view campaign analytics page
if st.button('View Campaign Analytics', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/03_Campaign_Resources.py')

# creating button redirecting manager to site feedback page
if st.button('Give PollPal some feedback!', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/04_Campaign_Survey.py')