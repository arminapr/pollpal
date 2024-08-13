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
def fetch_polling_data():
    try:
        polling_data = requests.get('http://api:4000/d/voter-info').json()
        return polling_data
    except:
        st.write("Could not connect to sample api, so using dummy data.")
        polling_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}


# Initialize session state if not already
if 'polling_data' not in st.session_state:
    st.session_state.polling_data = fetch_polling_data()


if st.button('Delete polling data where age < 18', type='primary', use_container_width=True):
    try:
        response = requests.delete('http://api:4000/d/voter-info').json()
        st.write("Invalid polling data deleted successfully.")
        st.session_state.polling_data = fetch_polling_data()

    except Exception as e:
        st.write("Could not connect to sample API to delete data")

# Display the updated data
st.dataframe(st.session_state.polling_data)
