import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome voter, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Visualize voter turnout data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Voter_Turnout.py')

if st.button('View voter opinion by demographic', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Demographics.py')

if st.button("Complete your voter information survey",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Voter_Survey.py')

if st.button("Get to know a candidate's policies",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Candidate_Policies.py')

if st.button("Give PollPal some feedback!",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/15_Site_Survey.py')


  def VoterTurnoutNav():
    st.sidebar.page_link("pages/11_Voter_Turnout.py", label="Voter Turnout", icon='📈')

def VoterDemographicsNav():
    st.sidebar.page_link("pages/12_Demographics.py", label="Voter Demographics", icon='🛜')

def SurveyNav():
    st.sidebar.page_link("pages/13_Voter_Survey.py", label="Voter Survey", icon='📖')

def PolicyNav():
    st.sidebar.page_link("pages/14_Candidate_Policies.py", label="Explore Policies", icon='💅')

def VoterFeedbackNav():
    st.sidebar.page_link("pages/15_Site_Survey.py", label="Feedback", icon='😊')


if st.session_state['role'] == 'voter':
            VoterTurnoutNav()
            VoterDemographicsNav() 
            SurveyNav()
            PolicyNav()
            VoterFeedbackNav()
