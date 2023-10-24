import os
# Install dependencies from requirements.txt
os.system("pip install -r requirements.txt")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

import pandas as pd

# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'f315c6bace724974b42a5b2477423a23'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'e6917aeeb4e946e1a0a5a372a6e51af9'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/8080'

# Initialize Spotipy with your authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", open_browser=False))

def get_track_suggestions(track_name, max_suggestions=5):
    # Search for track suggestions
    results = sp.search(q=track_name, type='track', limit=max_suggestions)

    # Extract track names and artist names from suggestions
    suggestions = [f"{track['name']} - {', '.join([artist['name'] for artist in track['artists']])}" for track in results['tracks']['items']]

    return suggestions

def get_track_uri(track_name):
    # Search for the track
    results = sp.search(q=track_name, type='track', limit=1)

    # Check if any tracks were found
    if results['tracks']['total'] == 0:
        print(f"No tracks found for '{track_name}'.")
        return None

    # Get the URI of the first track found
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri

def create_playlist(playlist_name):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    return playlist['id'], playlist

def add_tracks_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)

# Function to generate the Spotify link
def generate_spotify_link(playlist_id, access_token):
    return f"https://open.spotify.com/playlist/{playlist_id}?si={access_token}"

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

track_name = st.text_input("Enter a song name:")
show_suggestions = st.button("Show Suggestions")

if show_suggestions:
    if track_name:
        suggestions = get_track_suggestions(track_name)
        selected_track = st.selectbox("Select a song from the suggestions:", suggestions)

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

        # Add recommended tracks to the playlist
        add_tracks_to_playlist(playlist_id, track_uris)

        # Generate Spotify link
        access_token = sp.auth_manager.get_access_token()['access_token']
        spotify_link = generate_spotify_link(playlist_id, access_token)

        st.success(f"Playlist '{playlist_name}' created with {len(track_uris)} recommended tracks.")
        st.write("You can access your playlist here:")
        st.markdown(f"[{playlist_name}]({spotify_link})")

    else:
        st.error(f"No tracks found for '{track_name}'.")
