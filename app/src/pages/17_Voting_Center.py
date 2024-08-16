import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# getting locations of all voting centers
st.title('Find a Voting Center Near You')
response = requests.get('http://api:4000/v/voting-center')
if response.status_code == 200:
    voting_center_info = response.json()
    state_options = sorted(list(set(item['state'] for item in voting_center_info)))
else:
    st.error(f"Failed to retrieve states with voting centers. Status code: {response.status_code}")
    state_options = []

# allowing user to select a state
state = st.selectbox('Select the state you\'re in', state_options, index=None)
logger.info(f'var_01 = {state}')
logger.info(f'Retrieved data: {state_options}')

# allowing user to view voting centers in the selected state
if state != None and st.button('View voting centers in my state',
                              type='primary',
                              use_container_width=True):
    results = requests.get(f'http://api:4000/v/voting-center').json()
    df = pd.DataFrame(results)
    filtered_df = df[df['state'] == state]

    # Display the filtered DataFrame
    st.dataframe(filtered_df)