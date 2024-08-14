import logging
logger = logging.getLogger()
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title(f"Welcome System Administrator")
st.write('')
st.write('')

st.write("## Train the ML Model:")

if st.button('Train model',type='primary'):
    the_response = requests.get(f'http://web-api:4000/m/ml_models/train')
    logger.info(f'res = {the_response}')
    if the_response.status_code == 200:
        st.write('sucsess')
    else:
        st.write(the_response.status_code)
        st.write('fail')

    if st.button('Logout'):
        st.switch_page('Home.py')