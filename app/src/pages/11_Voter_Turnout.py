import logging
logger = logging.getLogger(__name__)

import streamlit as st
# TODO: implement SideBarLinks
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Voter Turnout by Election Year')
year_options = [2024, 2020, 2016, 2012, 2008, 2004, 2000]
year = st.selectbox('Select an election year', year_options, index=None)
logger.info(f'var_01 = {year}')

# add a button to use the values entered into the number field to send to the 
# prediction function via the REST API
if year != None and st.button('View voter turnout',
             type='primary',
             use_container_width=True):
  results = requests.get(f'http://api:4000/v/state-voters/{year}').json()
  st.dataframe(results)
  