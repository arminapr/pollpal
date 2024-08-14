import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import altair as alt
from modules.nav import SideBarLinks
import requests

SideBarLinks()
st.title("Campaign Analysis")

response = requests.get('http://api:4000/c/campaign-ids').json()
campaign_ids = [item['campaignId'] for item in response]

# dropdown for choosing the campaign id
selected_campaign_id = st.selectbox('Select Campaign ID', campaign_ids)

if selected_campaign_id is not None:
    if st.button(f'View campaign data for ID {selected_campaign_id}',
                 type='primary',
                 use_container_width=True):
        query_url = f'http://api:4000/c/campaign-data/{selected_campaign_id}'
        
        campaign_data = requests.get(query_url).json()
        df = pd.DataFrame(campaign_data)

        df['totalInteractions'] = df['totalInteractions'].astype(float)
        df['advertisementsCost'] = df['advertisementsCost'].astype(float)
        df['totalAttendees'] = df['totalAttendees'].astype(float)
        df['ralliesCost'] = df['ralliesCost'].astype(float)
        
        # ratios
        df['Advertisments'] = df['advertisementsCost'] / df['totalInteractions']
        df['Rallies'] = df['ralliesCost'] / df['totalAttendees']

        # display campaign details
        st.write(f"### Campaign ID: {selected_campaign_id}")
        st.write(df[['totalInteractions', 'advertisementsCost', 'totalAttendees', 'ralliesCost']])

        # display ratios
        st.write(f"### Ratio of Total Cost per Total Interaction")
        st.write(df[['Advertisments', 'Rallies']])
        
        # visualizing the ratios
        ratio_df = pd.melt(df[['Advertisments', 'Rallies']],
                           var_name='Metric', value_name='Cost')
        
        bar_chart = alt.Chart(ratio_df).mark_bar().encode(
            x=alt.X('Metric:N', title=''),
            y=alt.Y('Cost:Q', title='Cost vs Total Interaction'),
            color='Metric:N',
            tooltip=['Metric:N', 'Cost:Q']
        ).properties(
            width=alt.Step(80) 
        )

        # chart
        st.altair_chart(bar_chart, use_container_width=True)