import logging
logger = logging.getLogger()
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger.info('In the broken function')

st.title(f"Welcome System Administrator")
st.write('')
st.write('')

st.write("## Train the ML Model:")

if st.button('Train model',type='primary'):
    pre_results = requests.get(f'http://web-api1:4000/m/ml_models/train')
    logger.info(f'res = {pre_results}')
    if pre_results.status_code == 200:
        st.write('sucsess')
    else:
        st.write(pre_results.status_code)
        st.write('fail')

    if st.button('Logout'):
        st.switch_page('Home.py')