import streamlit as st
import requests
from modules.nav import SideBarLinks
import pandas as pd
import altair as alt

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Set the header of the page
st.header('Polling Data')

# Fetch election years from API
response = requests.get('http://api:4000/c/election-years').json()
years = [item['year'] for item in response]

# allowing user to select from a given set of years
selected_year = st.selectbox('Select Election Year', years)

# getting and displaying data for the selected year
if selected_year != None:
    if st.button(f'View polling data from {selected_year}',
                 type='primary',
                 use_container_width=True):
        voter_data = requests.get(f'http://api:4000/c/polling-data/{selected_year}').json()
        df = pd.DataFrame(voter_data)
        df['fullName'] = df['firstName'] + ' ' + df['lastName']

        # setting up color mapping for legend
        color_mapping = {
            'Democrat': 'blue',
            'Republican': 'red',
            'Independent': 'yellow'
        }

        # initializing bar chart using Altair
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('votes:Q', title='Votes'),
            x=alt.X('fullName:N', title='Candidate Name'),
            color=alt.Color('politicalAffiliation:N', scale=alt.Scale(domain=['Democrat', 'Republican', 'Independent'],
                                                                      range=['blue', 'red', 'yellow'])),
            tooltip=['fullName:N', 'votes:Q', 'politicalAffiliation:N']
        ).properties(
            title=f'Votes per Candidate in {selected_year}'
        )

        # displaying bar chart
        st.altair_chart(chart, use_container_width=True)