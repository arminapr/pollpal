import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Set the header of the page
st.header('Polling Data')

# Fetch election years from API
response = requests.get('http://api:4000/c/election-years').json()
years = [item['year'] for item in response]

# Allow user to select a year
selected_year = st.selectbox('Select Election Year', years)

# Fetch and display data for the selected year
if selected_year != None:
    if st.button(f'View polling data from {selected_year}',
                 type='primary',
                 use_container_width=True):
        voter_data = requests.get(f'http://api:4000/c/polling-data/{selected_year}').json()
        st.dataframe(voter_data)
