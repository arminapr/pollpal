import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd


st.set_page_config(layout = 'wide')

SideBarLinks()

m = st.markdown("""
<style>

div.stButton > button:first-child {
    background-color: rgb(0, 104, 201);
    border: 2px solid rgb(0, 104, 201)
    color:#ffffff;
    }

div.stButton > button:hover {
    background-color: rgb(255, 43, 43);
    border: 2px solid rgb(255, 43, 43);
    color: #ffffff;
}

</style>""", unsafe_allow_html=True)
st.title('Removing Invalid Polling Data')
"""
Polling Data
"""

# gets the polling data input by the voter user
def fetch_polling_data():
    try:
        polling_data = requests.get('http://api:4000/d/voter-info').json()
        return polling_data
    except:
        st.write("Could not connect to sample api, so using dummy data.")
        polling_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}


# initializing session state if not already
if 'polling_data' not in st.session_state:
    st.session_state.polling_data = fetch_polling_data()

# allowing user to delete polling data where age < 18
if st.button('Delete polling data where age < 18', type='primary', use_container_width=True):
    try:
        response = requests.delete('http://api:4000/d/voter-info').json()
        st.write("Invalid polling data deleted successfully.")
        st.session_state.polling_data = fetch_polling_data()

    except Exception as e:
        st.write("Could not connect to sample API to delete data")

# displaying cleaned data
df = pd.DataFrame(st.session_state.polling_data)
df = df[['voterId', 'age', 'votingCenterId', 'state', 'county', 'gender', 'politicalAffiliation']]
df.rename(columns={
            'voterId': 'PollPal Voter ID',
            'age': 'Age',
            'votingCenterId': 'Voting Center ID',
            'state': 'State',
            'county': 'County',
            'gender': 'Gender',
            'politicalAffiliation': 'Political Affiliation'
        }, inplace=True)

st.dataframe(df)

