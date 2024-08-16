# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolDataNav():
    st.sidebar.page_link("pages/01_Polling_Data.py", label="Real Time Polling Data", icon='📊')

def SwingStateNav():
    st.sidebar.page_link("pages/02_Swing_States.py", label="Find Swing States", icon='🔎')

def ResourceNav():
    st.sidebar.page_link("pages/03_Campaign_Resources.py", label="Campaign Resource Report", icon='📈')
    
def CampaignFeedbackNav():
    st.sidebar.page_link("pages/04_Campaign_Survey.py", label="Share Feedback", icon='😊')

## ------------------------ Role of voter ------------------------
def VoterTurnoutNav():
    st.sidebar.page_link("pages/11_Voter_Turnout.py", label="Voter Turnout", icon='📈')

def VoterDemographicsNav():
    st.sidebar.page_link("pages/12_Demographics.py", label="Voter Demographics", icon='🛜')

def VotingCenter():
   st.sidebar.page_link("pages/17_Voting_Center.py", label="Voting Center", icon='🏢')

def SurveyNav():
    st.sidebar.page_link("pages/13_Voter_Survey.py", label="Voter Survey", icon='📖')

def PolicyNav():
    st.sidebar.page_link("pages/14_Candidate_Policies.py", label="Explore Policies", icon='💅')

def VoterFeedbackNav():
    st.sidebar.page_link("pages/15_Site_Survey.py", label="Share Feedback", icon='😊')

def PredictPartyNav():
    st.sidebar.page_link("pages/16_Predict_Party.py", label="Predict Political Party", icon='🤔')

#### ------------------------ Data Analyst Role ------------------------
def InvalidDataNav():
    st.sidebar.page_link("pages/21_Clean_Inavlid_Data.py", label='Data Cleanup', icon='🏢')

def DemographicDataNav():
    st.sidebar.page_link("pages/22_Demographic_Data.py", label='Demographic Data', icon='📊')

def SurveyResponsesNav():
    st.sidebar.page_link("pages/23_User_Site_Surveys.py", label="User Feedback", icon='🧐')

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False, home_breadcrumb=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home and not st.session_state["authenticated"]:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state['role'] == 'campaign_manager':
            PolDataNav()
            SwingStateNav()
            ResourceNav()
            CampaignFeedbackNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'voter':
            VoterTurnoutNav()
            VoterDemographicsNav()
            VotingCenter()
            SurveyNav()
            PolicyNav()
            VoterFeedbackNav()
            PredictPartyNav()

        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'data_analyst':
            InvalidDataNav()
            DemographicDataNav()
            SurveyResponsesNav()

        if st.session_state['role'] == 'system_admin':
            SystemAdminNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    # https://discuss.streamlit.io/t/how-to-change-the
    # -backgorund-color-of-button-widget/12103/25?page=2
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(0, 104, 201);
        border: 2px solid rgb(0, 104, 201);
        color: #ffffff; 
    }

    div.stButton > button:hover {
        background-color: rgb(255, 43, 43);
        border: 2px solid rgb(255, 43, 43);
        color: #ffffff;
    }
    </style>""", unsafe_allow_html=True)
    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout!"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')
