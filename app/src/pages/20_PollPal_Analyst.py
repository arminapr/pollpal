import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# https://discuss.streamlit.io/t/how-to-change-the
# -backgorund-color-of-button-widget/12103/25?page=2
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

st.title(f"Welcome PollPal Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# redirecting analyst to delete invalid data page
if st.button('Delete Invalid Polling Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Clean_Inavlid_Data.py')

# redirecting analyst to view polling data by demographic page
if st.button('View Polling Data By Demographic',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Demographic_Data.py')

# redirecting analyst to view user site responses page
if st.button("View User Site Survey Responses",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_User_Site_Surveys.py')