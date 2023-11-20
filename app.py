import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
from streamlit_extras.buy_me_a_coffee import button

# Initialize the geolocator
geolocator = Nominatim(user_agent="SESOC-QM-Test")

def get_location(address):
    """ Get latitude and longitude of an address """
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

def create_map(latitude, longitude, radius=4000, zoom_start=12):
    """ Create a Folium map with a circle """
    map_ = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    folium.Marker([latitude, longitude]).add_to(map_)
    folium.LatLngPopup().add_to(map_)  # This allows users to click and see lat/long
    folium.Circle(
        radius=radius,
        location=[latitude, longitude],
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(map_)
    return map_

# Title for your app
st.title('Quincy\'s demo for SESOC')


# Initialize session state
if 'latitude' not in st.session_state or 'longitude' not in st.session_state:
    st.session_state['latitude'], st.session_state['longitude'] = -36.8529193, 174.7694239
    st.session_state['radius'] = 4000  # default radius in meters
    st.session_state['zoom'] = 12     # default zoom level

#Words for sidebar
st.sidebar.markdown('This sample script is a Proof-of-concept demonstrating the ability to search for an address, then running simply geopy python function to conduct some calculations. ')
st.sidebar.markdown('Two ways to use this page.   1) Use the search box to select a location of interest, or 2) double click on the map to find the GPS coordinate, then insert that into search box')
st.sidebar.header("Map controls")
# Slider for radius
radius_km = st.sidebar.slider("Radius (km)", 0, 50, int(st.session_state.radius / 1000), 1)
st.session_state.radius = radius_km * 1000  # convert km to meters

# Slider for zoom level
zoom_level = st.sidebar.slider("Zoom Level", 1, 18, st.session_state.zoom, 1)
st.session_state.zoom = zoom_level

# Search box for the address
address = st.sidebar.text_input('Enter an address or GPS coordinates')

if address:
    latitude, longitude = get_location(address)
    if latitude and longitude:
        st.session_state['latitude'], st.session_state['longitude'] = latitude, longitude

# Display the map
map_ = create_map(st.session_state.latitude, st.session_state.longitude, st.session_state.radius, st.session_state.zoom)
folium_static(map_)

# Display GPS coordinates
st.write(f"GPS Coordinates of selected point: Latitude {st.session_state['latitude']}, Longitude {st.session_state['longitude']}")


with st.sidebar:
    add_button=button(username="fake-username", floating=False, width=221)