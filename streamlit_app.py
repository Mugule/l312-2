import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# ---

prev_qry = ""

# ---

# Get coordinates from search bar
adresse = st.text_input("Adresse", "Paris")
r = "https://api-adresse.data.gouv.fr/search/?q=" + adresse
data = requests.get(r).json()
if data :
    coord = data["features"][0]["geometry"]["coordinates"]
    label = data["features"][0]["properties"]["label"]
    st.write(label + " - " + str(coord))
    user_query = data["features"][0]["geometry"]["coordinates"][::-1] # Default location PARIS and [::-1] reverse this shit x,y
else :
    st.write("no data")

# ---

# Function to get position from click coordinates
def get_pos(lat, lng):
    return lat, lng

# Initialize session state to store marker location
if "marker_location" not in st.session_state:
    st.session_state.marker_location = user_query
    st.session_state.zoom = 11  # Default zoom

# Create the base map
m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)

# Add a marker at the current location in session state
marker = folium.Marker(
    location=st.session_state.marker_location,
    draggable=False
)
marker.add_to(m)

# Render the map and capture clicks
map = st_folium(m, width=620, height=580, key="folium_map")

# Update marker position immediately after each click
if map.get("last_clicked") or (prev_qry != user_query):
    prev_qry = user_query
    lat, lng = map["last_clicked"]["lat"], map["last_clicked"]["lng"]
    st.session_state.marker_location = [lat, lng]  # Update session state with new marker location
    st.session_state.zoom = map["zoom"]
    # Redraw the map immediately with the new marker location
    m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
    folium.Marker(
        location=st.session_state.marker_location,
        draggable=False
    ).add_to(m)
    map = st_folium(m, width=400, height=250, key="folium_map")

# Display coordinates
st.write(f"Coordinates: {st.session_state.marker_location}")
