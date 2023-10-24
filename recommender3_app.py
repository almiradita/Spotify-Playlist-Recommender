import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os

# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'your_client_id'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'your_client_secret'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:8080'

# Initialize Spotipy with your authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", open_browser=False))

def get_artist_id(artist_name):
    # Search for the artist
    results = sp.search(q=artist_name, type='artist', limit=1)
    
    # Check if any artists were found
    if results['artists']['total'] == 0:
        print(f"No artist found for '{artist_name}'.")
        return None
    
    # Get the ID of the first artist found
    artist_id = results['artists']['items'][0]['id']
    return artist_id


# Streamlit app title and input fields
st.title("SpotiMix: Your Playlist Maker")

st.markdown(
    """
    Welcome to the Spotify Playlist Recommendation System! 🎵

    This app is your gateway to creating personalized Spotify playlists 
    based on your favorite artists. Whether you have a particular artist in mind
    or are looking for recommendations, we've got you covered.

    To get started, simply enter an artist's name in the input field below and explore
    a world of musical possibilities. We'll provide recommendations and let you
    craft the perfect playlist to match your mood.

    Let the music adventure begin! 🎶
    """
)

# Create a text input field for the artist's name
artist_name = st.text_input("Enter an artist's name:")

# Numeric input for the number of tracks to add
num_tracks_to_add = st.number_input("Number of tracks to add", min_value=1, max_value=50, value=10)

# Input field for the playlist name
playlist_name = st.text_input("Enter a playlist name:", "Recommended Playlist")  # Default name

if st.button("Create Playlist") and artist_name:
    # Get artist ID based on the artist's name
    artist_id = get_artist_id(artist_name)
    if artist_id:
        # Create a playlist and get playlist ID
        playlist_id, playlist = create_playlist(playlist_name)

        # Get recommended tracks based on the selected artist
        recommendations = get_recommendations_by_artist(artist_id)

        # Extract track URIs from recommendations
        track_uris = [track['uri'] for track in recommendations]

        # Limit the number of tracks to add based on user input
        track_uris = track_uris[:num_tracks_to_add]

        # Add recommended tracks to the playlist
        add_tracks_to_playlist(playlist_id, track_uris)

        st.success(f"Playlist '{playlist_name}' created with {len(track_uris)} recommended tracks.")
