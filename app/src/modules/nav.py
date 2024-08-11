# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link("pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon='👤')

def WorldBankVizNav():
    st.sidebar.page_link("pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon='🏦')

def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon='🗺️')

## ------------------------ Role of voter ------------------------
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

#### ------------------------ Data Analyst Role ------------------------
def InvalidDataNav():
    st.sidebar.page_link("pages/21_Clean_Inavlid_Data.py", label='Data Cleanup', icon='🏢')

def DemographicDataNav():
    st.sidebar.page_link("pages/22_Demographic_Data.py", label='Demographic Data', icon='📊')

def SurveyResponsesNav():
    st.sidebar.page_link("pages/23_User_Site_Surveys.py", label="User Feedback", icon='🧐')

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state['role'] == 'campaign_manager':
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'voter':
            VoterTurnoutNav()
            VoterDemographicsNav() 
            SurveyNav()
            PolicyNav()
            VoterFeedbackNav()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'data_analyst':
            InvalidDataNav()
            DemographicDataNav()
            SurveyResponsesNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

