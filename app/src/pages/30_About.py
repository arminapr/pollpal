import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

st.write("# About this App")

st.markdown (
    """
    This is a PollPal app for the CS 3200 Course Project.  
    Founded by Armina Parvaresh Rizi, Nalika Palayoor, Niki Anand, Celia Burrington & Sriya Vuppala.

    The goal of this application is to help users stay informed on current
    election information and make informed decisions for managing campaigns. 
    This application relies on three users who take on the roles of campaign manager,
    voter, and data analyst. Note that this application only uses mock data and 
    should not be used for actual election information. 
    
    Thank you for visiting PollPal!
    """
        )
