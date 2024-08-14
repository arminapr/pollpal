import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout='wide')

# Assuming SideBarLinks() is defined somewhere
from modules.nav import SideBarLinks

SideBarLinks()

st.title('Site Survey Responses Page')
"""
Voter responses
"""

# getting and displaying voter data
try:
    voter_data = requests.get('http://api:4000/d/voter-site-survey').json()
except requests.RequestException:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    voter_data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
voter_df = pd.DataFrame(voter_data)
st.dataframe(voter_df)

# calculate and display averages for some voter data
if 'foundNeededInfo' in voter_df.columns and 'isUserFriendly' in voter_df.columns:
    voter_df['foundNeededInfo'] = pd.to_numeric(voter_df['foundNeededInfo'], errors='coerce')
    voter_df['isUserFriendly'] = pd.to_numeric(voter_df['isUserFriendly'], errors='coerce')

    avg_found_needed_info = voter_df['foundNeededInfo'].mean()
    avg_is_user_friendly = voter_df['isUserFriendly'].mean()

    # creating columns to make st.writes side by side
    # https://docs.streamlit.io/develop/api-reference/layout/st.columns
    col1, col2 = st.columns(2)

    with col1:
     st.write(f"**Average rating for 'foundNeededInfo':** {avg_found_needed_info:.2f}")

    with col2:
     st.write(f"**Average rating for 'isUserFriendly':** {avg_is_user_friendly:.2f}")

st.write('\n\n')
"""
Campaign manager responses
"""

# getting and displaying campaign manager data
try:
    camp_data = requests.get('http://api:4000/d/campaign-site-survey').json()
except requests.RequestException:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    camp_data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

camp_df = pd.DataFrame(camp_data)
st.dataframe(camp_df)

# calculating and displaying avg stats for campaign manager data
if 'foundNeededInfo' in camp_df.columns and 'isUserFriendly' in camp_df.columns:
    camp_df['foundNeededInfo'] = pd.to_numeric(camp_df['foundNeededInfo'], errors='coerce')
    camp_df['isUserFriendly'] = pd.to_numeric(camp_df['isUserFriendly'], errors='coerce')

    avg_found_needed_info = camp_df['foundNeededInfo'].mean()
    avg_is_user_friendly = camp_df['isUserFriendly'].mean()

    # creating columns to make st.writes side by side
    # https://docs.streamlit.io/develop/api-reference/layout/st.columns
    col3, col4 = st.columns(2)
    with col3:
        st.write(f"**Average rating for 'foundNeededInfo':** {avg_found_needed_info:.2f}")

    with col4:
        st.write(f"**Average rating for 'isUserFriendly':** {avg_is_user_friendly:.2f}")




