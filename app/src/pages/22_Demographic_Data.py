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

# allowing user to pick a demographic they want insights into
demographic = st.selectbox( 'Which voter demographic would you like insights into?',
 ('gender', 'ethnicity', 'age'))

# defining endpoints based on selected demographic
if demographic == 'ethnicity':
    endpoint = '/voter-info-ethnicity'
elif demographic == 'age':
    endpoint = '/voter-info-age'
else:
    endpoint = '/voter-info-gender'

# getting polling data related to selected demographic
base_url = 'http://api:4000/d'
results = requests.get(base_url+endpoint).json()

# organizing age data into different age ranges
if demographic == 'age':
    # defining age ranges
    age_ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 70), (71, 80), (81, 90), (91, 100)]
    grouped_data = {}
    # grouping data into defined age ranges
    for item in results:
        age = item['age']
        user_count = item['userCount']
        for age_range in age_ranges:
            if age_range[0] <= age <= age_range[1]:
                range_label = f'{age_range[0]}-{age_range[1]}'
                # initializing new age label if it doesn't exist
                if range_label not in grouped_data:
                    grouped_data[range_label] = 0
                grouped_data[range_label] += user_count
                break

    # converting grouped data to a list of dictionaries
    results = [{'age': k, 'userCount': v} for k, v in grouped_data.items() if v > 0]

# finding maximum count of voters per demographic category
max_possible_count = max(item['userCount'] for item in results)

# allowing user to select minimum number of people in each category to display
min_count = st.number_input(
    'Select the minimum number of people in each category to display:',
    min_value=1,
    max_value=max_possible_count,
    value=1
)

# filtering data based on selected minimum count
filtered_data = [item for item in results if item['userCount'] >= min_count]

# defining labels and values from data
labels = [item[demographic] for item in filtered_data]
values = [item['userCount'] for item in filtered_data]

# creating pie chart
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# displaying pie chart
st.pyplot(fig)
