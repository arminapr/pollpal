import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a demo app for the CS 3200 Course Project.  

    The goal of this demo is to navigate an application
    catered towards three different personas. Each page
    addresses a persona's user story.

    Stay tuned for more information and features to come!
    """
        )
