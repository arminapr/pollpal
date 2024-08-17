import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from modules.nav import SideBarLinks

SideBarLinks()

# set up the page
st.header("Identify Swing States")
st.write("The data below reflects swing states since 1984")
# getting data
response = requests.get('http://api:4000/c/swing-state')

# dictionary for state coordinates
state_coordinates = {
    'alabama': (32.806671, -86.791130),
    'alaska': (61.370716, -152.404419),
    'arizona': (33.729759, -111.431221),
    'arkansas': (34.969704, -92.373123),
    'california': (36.116203, -119.681564),
    'colorado': (39.059811, -105.311104),
    'connecticut': (41.597782, -72.755371),
    'delaware': (39.318523, -75.507141),
    'florida': (27.766279, -81.686783),
    'georgia': (33.040619, -83.643074),
    'hawaii': (21.371257, -157.138423),
    'idaho': (44.299782, -114.513282),
    'illinois': (40.673976, -89.398528),
    'indiana': (39.849426, -86.258278),
    'iowa': (42.011539, -93.210526),
    'kansas': (37.966406, -95.665381),
    'kentucky': (37.668140, -84.670067),
    'louisiana': (31.169546, -91.867805),
    'maine': (44.693947, -69.381927),
    'maryland': (39.063946, -76.802101),
    'massachusetts': (42.230171, -71.530106),
    'michigan': (43.326618, -84.536095),
    'minnesota': (45.694454, -93.900192),
    'mississippi': (32.741646, -89.678696),
    'missouri': (38.456085, -92.288368),
    'montana': (46.921925, -110.454353),
    'nebraska': (41.125370, -98.268082),
    'nevada': (38.313515, -117.055374),
    'new hampshire': (43.452492, -71.563896),
    'new jersey': (40.298904, -74.521011),
    'new mexico': (34.840515, -106.248482),
    'new york': (42.165726, -74.948051),
    'north carolina': (35.630066, -79.806419),
    'north dakota': (47.528912, -99.784012),
    'ohio': (40.388783, -82.764915),
    'oklahoma': (35.565342, -96.928917),
    'oregon': (44.572021, -122.070938),
    'pennsylvania': (40.590752, -77.209755),
    'rhode island': (41.680893, -71.511780),
    'south carolina': (33.856892, -80.945007),
    'south dakota': (44.299782, -99.438828),
    'tennessee': (35.747845, -86.692345),
    'texas': (31.054487, -97.563461),
    'utah': (40.150032, -111.862434),
    'vermont': (44.045876, -72.710686),
    'virginia': (37.769337, -78.169968),
    'washington': (47.400902, -121.490494),
    'west virginia': (38.491226, -80.954201),
    'wisconsin': (44.268543, -89.616508),
    'wyoming': (42.755966, -107.302490)
}

# converting json data to dataframe
if response.status_code == 200:
    if response.content:
        data = response.json()
        df = pd.DataFrame(data)
        df = df[['stateName', 'stateAbbr', 'year', 'partyRepresentative', 'popularVoteRatio', 'numElectoralVotes']]

        df.rename(columns={
            'stateAbbr': 'State Abbreviation',
            'stateName': 'State Name',
            'popularVoteRatio': 'Popular Vote Ratio (Winning : Other)',
            'partyRepresentative': 'Party Representative',
            'numElectoralVotes': 'Electoral Votes',
            'year': 'Year'
        }, inplace=True)

        # reordering the columns
        df['Year'] = df['Year'].astype(int).astype(str) 
        df['Popular Vote Ratio (Winning : Other)'] = (df['Popular Vote Ratio (Winning : Other)'] * 100).map("{:.2f}%".format)
        
        st.dataframe(df)
        
        df['latitude'] = None
        df['longitude'] = None

        # the below code is to show a map of where the states are
        for index, row in df.iterrows():
            state_name = row['State Name'].lower()
            if state_name in state_coordinates:
                df.at[index, 'latitude'], df.at[index, 'longitude'] = state_coordinates[state_name]
        
        # check if the latitude and longitude for all states were added
        if df['latitude'].notna().all() and df['longitude'].notna().all():
            layer = pdk.Layer(
                "ScatterplotLayer",
                df,
                get_position=["longitude", "latitude"],
                get_radius=100000,
                get_color=[255, 0, 0],
                pickable=True,
            )

            view_state = pdk.ViewState(
                latitude=df['latitude'].mean(),
                longitude=df['longitude'].mean(),
                zoom=3,
                pitch=0,
            )

            # rendering the map
            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
        else:
            st.write("Unable to fetch latitude and longitude for some states.")
    else:
        st.write("Response is empty")
else:
    st.write("Error response:", response.status_code)
    
