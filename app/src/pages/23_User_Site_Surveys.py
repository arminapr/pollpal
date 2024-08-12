import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Site Survey Responses Page')
"""
Voter responses

"""
voter_data = {} 
try:
  voter_data = requests.get('http://api:4000/d/voter-site-survey').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  voter_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(voter_data)

"""
Campaign manager responses

"""
camp_data = {} 
try:
  camp_data = requests.get('http://api:4000/d/campaign-site-survey').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  camp_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(camp_data)