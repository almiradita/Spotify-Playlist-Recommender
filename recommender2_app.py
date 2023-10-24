import os
# Install dependencies from requirements.txt
os.system("pip install -r requirements.txt")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'your_client_id'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'your_client_secret'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8080'

# Initialize Spotipy with your authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", open_browser=False))

# Streamlit app title and input fields
st.title("SpotiMix: Your Playlist Maker")

st.markdown(
    """
    Welcome to the Spotify Playlist Recommendation System! 🎵

    This app is your gateway to creating personalized Spotify playlists 
    based on your favorite songs. Whether you have a particular track in mind
    or are looking for recommendations, we've got you covered.

    To get started, simply enter a song name in the input field below and explore
    a world of musical possibilities. We'll provide suggestions and let you
    craft the perfect playlist to match your mood.

    Let the music adventure begin! 🎶
    """
)

# Create a text input field for the song name
track_name = st.text_input("Enter a song name:")

# Fetch and display track suggestions as the user types
if track_name:
    suggestions = get_track_suggestions(track_name)
    selected_track = st.selectbox("Select a song from the suggestions:", suggestions)

# Numeric input for the number of tracks to add
num_tracks_to_add = st.number_input("Number of tracks to add", min_value=1, max_value=50, value=10)

# Input field for the playlist name
playlist_name = st.text_input("Enter a playlist name:", "Recommended Playlist")  # Default name

if st.button("Create Playlist") and track_name:
    # Get track URI of the selected track
    track_uri = get_track_uri(track_name)
    if track_uri:
        # Create a playlist and get playlist ID
        playlist_id, playlist = create_playlist(playlist_name)

        # Get recommended tracks based on the selected track
        recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']

        # Extract track URIs from recommendations
        track_uris = [track['uri'] for track in recommendations]

        # Limit the number of tracks to add based on user input
        track_uris = track_uris[:num_tracks_to_add]

        # Add recommended tracks to the playlist
        add_tracks_to_playlist(playlist_id, track_uris)

        st.success(f"Playlist '{playlist_name}' created with {len(track_uris)} recommended tracks.")
