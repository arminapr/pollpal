import streamlit as st
import requests
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the URL for the Flask backend
FLASK_URL = 'http://web-api:4000/p/ml_models/1'

st.write("### Train an ML Model:")

# Button to trigger model training
if st.button('Train Model', type='primary', use_container_width=True):
    try:
        # Make the GET request to the Flask backend
        pre_results = requests.get(FLASK_URL)
        logger.info(f'res = {pre_results}')
        
        # Check if the request was successful
        if pre_results.status_code == 200:
            st.write('Model trained: success :)')
        else:
            st.write('Model trained: failed :(')
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        st.write(f'Error occurred: {e}')
        logger.error(f'Error occurred: {e}')

# Button to logout
if st.button("Logout"):
    st.write("Logging out...")
    # Add logic for logout if necessary
    st.experimental_rerun()  # Redirect or refresh the page
