import googlemaps
import streamlit as st

APIKEY = st.secrets.GOOGLEMAP
gmaps = googlemaps.Client(key=APIKEY)
