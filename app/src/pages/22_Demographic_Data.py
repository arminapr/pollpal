import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('View Voter Demographics')

st.write('\n\n')

demographic = st.selectbox( 'Which voter demographic would you like insights into?',
 ('gender', 'ethnicity', 'age'))

# Define the API endpoint based on the selection
if demographic == 'ethnicity':
    endpoint = '/voter-info-ethnicity'
elif demographic == 'age':
    endpoint = '/voter-info-age'
else:
    endpoint = '/voter-info-gender'


base_url = 'http://api:4000/d'
results = requests.get(base_url+endpoint).json()
data = results


# Extract labels and values from the data
labels = [item[demographic] for item in data]
values = [item['userCount'] for item in data]

# Plot the pie chart
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart in Streamlit
st.pyplot(fig)
