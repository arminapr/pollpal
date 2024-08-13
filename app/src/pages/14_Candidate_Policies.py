import logging
logger = logging.getLogger(__name__)

import streamlit as st
# TODO: implement SideBarLinks
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Candidate Policy Stances')

candidate_data = {} 
try:
  candidate_data = requests.get('http://api:4000/v/policies/12').json() # <candidate-id in place of 12
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  candidate_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(candidate_data)
