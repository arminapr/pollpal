import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import matplotlib.pyplot as plt
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Opinion Data by Voter Demographic")

# add a button to use the values entered into the number field to send to the 
# prediction function via the REST API
def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    plt.title(title)
    return fig

political_affiliations = ['Republican', 'Democrat', 'Independent']
selected_affiliation = st.selectbox("Select Political Affiliation", political_affiliations)

show_visualization = st.checkbox("Show Visualization", value=True)

eResults = requests.get('http://api:4000/v/voter-info-ethnicity').json()
gResults = requests.get('http://api:4000/v/voter-info-gender').json()
aResults = requests.get('http://api:4000/v/voter-info-age').json()

filtered_ethnicity = [item for item in eResults if item['politicalAffiliation'] == selected_affiliation]
filtered_gender = [item for item in gResults if item['politicalAffiliation'] == selected_affiliation]
filtered_age = [item for item in aResults if item['politicalAffiliation'] == selected_affiliation]

if show_visualization:
    # Ethnicity Pie Chart
    st.write("### By Ethnicity")
    ethnicity_labels = [item['voterEthnicity'] for item in filtered_ethnicity]
    ethnicity_data = [item['numVotersByEthnicity'] for item in filtered_ethnicity]
    ethnicity_fig = create_pie_chart(ethnicity_data, ethnicity_labels, f'Opinion Data by Ethnicity ({selected_affiliation})')
    st.pyplot(ethnicity_fig)

    # Gender Pie Chart
    st.write("### By Gender")
    gender_labels = [item['voterGender'] for item in filtered_gender]
    gender_data = [item['numVotersByGender'] for item in filtered_gender]
    gender_fig = create_pie_chart(gender_data, gender_labels, f'Opinion Data by Gender ({selected_affiliation})')
    st.pyplot(gender_fig)

    # Age Pie Chart
    st.write("### By Age")
    age_labels = [item['voterAge'] for item in filtered_age]
    age_data = [item['numVotersByAge'] for item in filtered_age]
    age_fig = create_pie_chart(age_data, age_labels, f'Opinion Data by Age ({selected_affiliation})')
    st.pyplot(age_fig)
else:
    st.write("### By Ethnicity")
    st.dataframe(filtered_ethnicity)
    
    st.write("### By Gender")
    st.dataframe(filtered_gender)
    
    st.write("### By Age")
    st.dataframe(filtered_age)