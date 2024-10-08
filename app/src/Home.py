import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

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



# https://discuss.streamlit.io/t/colored-text/34892
st.title(':red[PollPal] - :blue[the Election Analysis App]')

st.write('\n\n')
st.write('### Welcome! As which user would you like to log in?')

# creating button to mimic campaign manager log-in
if st.button("Act as Alex Smith, a Campaign Manager",
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'campaign_manager'
    st.session_state['first_name'] = 'Alex'
    st.switch_page('pages/00_Campaign_Manager.py')

# creating button to mimic voter log-in
if st.button('Act as Sarah Sullivan, a Voter', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'voter'
    st.session_state['first_name'] = 'Sarah'
    st.switch_page('pages/10_Voter.py')

# creating button to mimic data-analyst log in
if st.button('Act as Michelle Rang, a Poll-Pal Data Analyst',
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'Michelle'
    st.switch_page('pages/20_PollPal_Analyst.py')



