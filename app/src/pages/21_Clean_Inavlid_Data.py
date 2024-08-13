import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Removing Invalid Polling Data')
"""
Polling Data
"""
polling_data = {}
try:
  polling_data = requests.get('http://api:4000/d/voter-info').json()
except Exception as e:
  st.write("Could not connect to sample api, so using dummy data.")

  polling_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
  print(e)

st.dataframe(polling_data)

st.button('Delete polling data where age < 18',
            type = 'primary',
            use_container_width=True)

