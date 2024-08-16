import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
# TODO: implement SideBarLinks
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()
st.title('Voter Turnout by Election Year')

# getting election year data
response = requests.get('http://api:4000/v/election-years')
if response.status_code == 200:
    election_year_info = response.json()
    year_options = [item['year'] for item in election_year_info]
else:
    st.error(f"Failed to retrieve election years. Status code: {response.status_code}")
    year_options = []
    election_year_info= [] 

# allowing user to select an election year
year = st.selectbox('Select an election year', year_options, index=None)
logger.info(f'var_01 = {year}')

# getting voter turn out based on selected year
if year != None and st.button('View voter turnout',
             type='primary',
             use_container_width=True):
  results = requests.get(f'http://api:4000/v/state-voters/{year}').json()

 
 # Convert results to a DataFrame
  df = pd.DataFrame(results)

  # Check if data is available and displaying bar chart
  if not df.empty:
    df.columns = ['State', 'Voter Turnout']
    st.bar_chart(df.set_index('State'), y_label='% turnout of voters', x_label='state')
  else:
    st.warning('No data available for the selected year.')
  
