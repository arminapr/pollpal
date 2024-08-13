import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Opinion Data by Voter Demographic")

# add a button to use the values entered into the number field to send to the 
# prediction function via the REST API

""" By ethnicity """
eResults = requests.get('http://api:4000/v/voter-info-ethnicity').json()
st.dataframe(eResults)
""" By gender """
gResults = requests.get('http://api:4000/v/voter-info-gender').json()
st.dataframe(gResults)
""" By age """
aResults = requests.get('http://api:4000/v/voter-info-age').json()
st.dataframe(aResults)