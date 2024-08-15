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

if demographic == 'age':
    # Define age ranges
    age_ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 70), (71, 80), (81, 90), (91, 100)]

    # Create a dictionary to hold the grouped data
    grouped_data = {}

    # Group the results into the defined age ranges
    for item in results:
        age = item['age']
        user_count = item['userCount']
        for age_range in age_ranges:
            if age_range[0] <= age <= age_range[1]:
                range_label = f'{age_range[0]}-{age_range[1]}'
                # Initialize the range label in the dictionary if it doesn't exist
                if range_label not in grouped_data:
                    grouped_data[range_label] = 0
                grouped_data[range_label] += user_count
                break

    # Convert the grouped data to a list of dictionaries
    results = [{'age': k, 'userCount': v} for k, v in grouped_data.items() if v > 0]

# Find the maximum count in the results
max_possible_count = max(item['userCount'] for item in results)

# Add an input for minimum category count
min_count = st.number_input(
    'Select the minimum number of people in each category to display:',
    min_value=1,
    max_value=max_possible_count,
    value=1
)

# Filter data based on the minimum count
filtered_data = [item for item in results if item['userCount'] >= min_count]



# Extract labels and values from the data
labels = [item[demographic] for item in filtered_data]
values = [item['userCount'] for item in filtered_data]

# Plot the pie chart
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart in Streamlit
st.pyplot(fig)
