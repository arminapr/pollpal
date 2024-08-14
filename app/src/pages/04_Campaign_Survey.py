import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Site Feedback')

response = requests.get('http://api:4000/c/campaign-ids')

if response.status_code == 200:
    campaign_ids_dict = response.json() 
    campaignIds = sorted([item['campaignId'] for item in campaign_ids_dict])
else:
    st.error(f"Failed to retrieve campaign IDs. Status code: {response.status_code}")
    campaignIds = []

with st.form(key='input_form'):
  campaignId = st.selectbox("Select Campaign ID", campaignIds)
  discoveredWhere = st.text_input("Where did you discover our page?")
  addAdditionalData = st.text_area("What additional data would have been helpful for PollPal to provide?")
  isDataUseful = st.radio("Was the data provided by PollPal useful for your campaign efforts?", ('True', 'False'))
  foundNeededInfo = st.slider("On a scale of 1-10, how user friendly was the site?", min_value=1, max_value=10, step=1)
  isUserFriendly = st.slider("On a scale of 1-10, how much of the info we provided, met your needs?", min_value=1, max_value=10, step=1)
  submitted = st.form_submit_button("Submit")

if submitted:
  data = {}
  data['campaignId'] = campaignId
  data['discoveredWhere'] = discoveredWhere
  data['addAdditionalData'] = addAdditionalData
  data['isDataUseful'] = isDataUseful
  data['foundNeededInfo'] = foundNeededInfo
  data['isUserFriendly'] = isUserFriendly
  st.write(data)
  
  response = requests.post('http://api:4000/c/campaign-site-survey', json=data)
  if response.status_code == 200:
    st.success('Campaign survey response submitted!')
  else:
    st.error(f"Failed to submit survey. Status code: {response.status_code}")