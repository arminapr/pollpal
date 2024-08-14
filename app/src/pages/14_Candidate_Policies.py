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

response = requests.get('http://api:4000/v/all-candidate-names')
if response.status_code == 200:
    candidate_info = response.json()
    candidate_names = sorted(
        [f"{item['candidateId']} {item['firstName']} {item['lastName']}" for item in candidate_info],
        key=lambda name: name.split()[2] 
    )    
    candidate_id = sorted([candidate['candidateId'] for candidate in candidate_info])
else:
    st.error(f"Failed to retrieve candidate info. Status code: {response.status_code}")
    candidate_names = []
    
# choose the candidate's name
selected_candidate_name = st.selectbox('Select a candidate (sorted by last name):', candidate_names)

# extract candidate ID from selected candidate name
selected_candidate_id = None
if selected_candidate_name:
    selected_candidate_id = int(selected_candidate_name.split()[0])

candidate_data = {} 
try:
  candidate_data = requests.get(f'http://api:4000/v/policies/{selected_candidate_id}').json()
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  candidate_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
  
st.header("**Policies and Stances:**")
for policy in candidate_data:
    st.write(f"**Policy Name:** {policy['policyName']}")
    st.write(f"**Stance:** {policy['stance']}")
    st.write("---") 
