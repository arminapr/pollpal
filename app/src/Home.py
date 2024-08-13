import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

st.title('The Profs App')

st.write('\n\n')
st.write('### HI! As which user would you like to log in?')

if st.button("Act as Alex Smith, a Campaign Manager",
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'campaign_manager'
    st.session_state['first_name'] = 'Alex'
    st.switch_page('pages/00_Campaign_Manager.py')

if st.button('Act as Sarah Sullivan, a Voter', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'voter'
    st.session_state['first_name'] = 'Sarah'
    st.switch_page('pages/10_Voter.py')

if st.button('Act as Michelle, a PollPal Data Analyst',
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'Michelle'
    st.switch_page('pages/20_PollPal_Analyst.py')

if st.button('System Admin', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.switch_page('pages/40_SysAdmin.py')



