import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
import altair as alt

st.set_page_config(layout='wide')

# Assuming SideBarLinks() is defined somewhere
from modules.nav import SideBarLinks

SideBarLinks()

st.title('Site Survey Responses Page')
"""
Voter responses
"""

show_voter_index = st.checkbox("Show Voter Response Column Descriptions")

if show_voter_index:
    st.markdown("""
    **Voter Response Column Descriptions:**
    - **PollPal Voter ID**: The unique identifier for each voter in the PollPal system.
    - **Discovered Where**: Where the voter found out about the PollPal page.
    - **Found Needed Info (1-10)**: The voter's rating on how well they found the needed information.
    - **Is User Friendly (1-10)**: The voter's rating on the site's user-friendliness.
    - **Informed About Candidate**: Whether the voter feels informed about the candidates.
    - **Found Voting Center**: Whether the voter found a voting center through the site.
    - **Date Filled Out**: The date the survey was completed.
    - **Date Updated**: The date the survey was last updated.
    """)

# getting and displaying voter data
try:
    voter_data = requests.get('http://api:4000/d/voter-site-survey').json()
except requests.RequestException:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    voter_data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
voter_df = pd.DataFrame(voter_data)
voter_df = voter_df[['voterSurveyId', 'voterId', 'discoveredWhere', 'foundNeededInfo', 'isUserFriendly', 'informedAboutCandidate', 'foundVotingCenter', 'createdAt', 'updatedAt']]
voter_df['foundVotingCenter'] = voter_df['foundVotingCenter'].astype(bool)
voter_df['informedAboutCandidate'] = voter_df['informedAboutCandidate'].astype(bool)

visualize_voter = st.checkbox("Show Voter Response Visualization")

# calculate and display averages for some voter data
if 'foundNeededInfo' in voter_df.columns and 'isUserFriendly' in voter_df.columns:
    voter_df['foundNeededInfo'] = pd.to_numeric(voter_df['foundNeededInfo'], errors='coerce')
    voter_df['isUserFriendly'] = pd.to_numeric(voter_df['isUserFriendly'], errors='coerce')

    avg_found_needed_info = voter_df['foundNeededInfo'].mean()
    avg_is_user_friendly = voter_df['isUserFriendly'].mean()
    if visualize_voter:
      user_friendly_chart = alt.Chart(voter_df).mark_bar().encode(
        x=alt.X('isUserFriendly:Q', bin=alt.Bin(maxbins=10), title='Score'),
        y=alt.Y('count()', title='Count')
      ).properties(
          title='Is User Friendly (1-10) Distribution'
      )

      needed_info_chart = alt.Chart(voter_df).mark_bar().encode(
        x=alt.X('foundNeededInfo:Q', bin=alt.Bin(maxbins=10), title='Score'),
        y=alt.Y('count()', title='Count')
      ).properties(
          title='Found Needed Info (1-10) Distribution'
      )

      # display the finding needed info chart
      st.altair_chart(needed_info_chart, use_container_width=True)
      # display the user friendly scale chart
      st.altair_chart(user_friendly_chart, use_container_width=True)
      
    # creating columns to make st.writes side by side
    # https://docs.streamlit.io/develop/api-reference/layout/st.columns
    col1, col2 = st.columns(2)

    with col1:
     st.write(f"**Average rating for 'foundNeededInfo':** {avg_found_needed_info:.2f}")

    with col2:
     st.write(f"**Average rating for 'isUserFriendly':** {avg_is_user_friendly:.2f}")
voter_df.rename(columns={
                  'createdAt': 'Date Filled Out',
                  'updatedAt': 'Date Updated',
                  'discoveredWhere': 'Discovered Where',
                  'foundNeededInfo': 'Found Needed Info (1-10)',
                  'isUserFriendly': 'Is User Friendly (1-10)',
                  'foundVotingCenter': 'Found Voting Center',
                  'informedAboutCandidate': 'Informed About Candidate',
                  'voterId': 'PollPal Voter ID',
                  'voterSurveyId': 'Survey ID'
                }, inplace=True)
st.dataframe(voter_df)
st.write('\n\n')
"""
Campaign manager responses
"""

show_campaign_index = st.checkbox("Show Campaign Manager Response Column Descriptions")

if show_campaign_index:
    st.markdown("""
    **Campaign Manager Response Column Descriptions:**
    - **Campaign ID**: The unique identifier for each campaign.
    - **Discovered Where**: Where the campaign manager found out about the PollPal page.
    - **Found Needed Info (1-10)**: The campaign manager's rating on how well they found the needed information.
    - **Is User Friendly (1-10)**: The campaign manager's rating on the site's user-friendliness.
    - **Is Data Useful?**: Whether the data provided by PollPal was useful for the campaign efforts.
    - **Additional Features Proposed**: Suggestions for additional features that would have been helpful.
    - **Date Filled Out**: The date the survey was completed.
    - **Date Updated**: The date the survey was last updated.
    """)

# getting and displaying campaign manager data
try:
    camp_data = requests.get('http://api:4000/d/campaign-site-survey').json()
except requests.RequestException:
    st.write("**Important**: Could not connect to sample API, so using dummy data.")
    camp_data = {"a": {"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

camp_df = pd.DataFrame(camp_data)
camp_df['isDataUseful'] = camp_df['isDataUseful'].astype(bool)
ca_avg_found_needed_info = camp_df['foundNeededInfo'].mean()
ca_avg_is_user_friendly = camp_df['isUserFriendly'].mean()
camp_df = camp_df[['campaignSurveyId', 'campaignId', 'discoveredWhere', 'foundNeededInfo', 'isUserFriendly', 'isDataUseful', 'addAdditionalData', 'createdAt', 'updatedAt']]

visualize_campaign = st.checkbox("Show Campaign Manager Response Visualization")

if visualize_campaign:
  ca_user_friendly_chart = alt.Chart(camp_df).mark_bar().encode(
    x=alt.X('isUserFriendly:Q', bin=alt.Bin(maxbins=10), title='Score'),
    y=alt.Y('count()', title='Count')
  ).properties(
      title='Is User Friendly (1-10) Distribution'
  )

  ca_needed_info_chart = alt.Chart(camp_df).mark_bar().encode(
    x=alt.X('foundNeededInfo:Q', bin=alt.Bin(maxbins=10), title='Score'),
    y=alt.Y('count()', title='Count')
  ).properties(
      title='Found Needed Info (1-10) Distribution'
  )


  # calculating and displaying avg stats for campaign manager data
  if 'foundNeededInfo' in camp_df.columns and 'isUserFriendly' in camp_df.columns:
      camp_df['foundNeededInfo'] = pd.to_numeric(camp_df['foundNeededInfo'], errors='coerce')
      camp_df['isUserFriendly'] = pd.to_numeric(camp_df['isUserFriendly'], errors='coerce')

      ca_avg_found_needed_info = camp_df['foundNeededInfo'].mean()
      ca_avg_is_user_friendly = camp_df['isUserFriendly'].mean()

      st.altair_chart(ca_needed_info_chart, use_container_width=True)
      st.altair_chart(ca_user_friendly_chart, use_container_width=True)

      col3, col4 = st.columns(2)
      with col3:
          st.write(f"**Average rating for 'foundNeededInfo':** {ca_avg_found_needed_info:.2f}")

      with col4:
          st.write(f"**Average rating for 'isUserFriendly':** {ca_avg_is_user_friendly:.2f}")

camp_df.rename(columns={
                  'createdAt': 'Date Filled Out',
                  'updatedAt': 'Date Updated',
                  'discoveredWhere': 'Discovered Where',
                  'foundNeededInfo': 'Found Needed Info (1-10)',
                  'isUserFriendly': 'Is User Friendly (1-10)',
                  'addAdditionalData': 'Additional Features Proposed',
                  'isDataUseful': 'Is Data Useful?',
                  'campaignId': 'Campaign ID',
                  'campaignSurveyId': 'Survey ID'
                }, inplace=True)
st.dataframe(camp_df)


