import os
# Install dependencies from requirements.txt
os.system("pip install -r requirements.txt")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st



# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = '019dae7245ac49459bb07f020206a7c4'
os.environ["SPOTIPY_CLIENT_SECRET"] = '243fa58269414cc6977815dbca6b9ef9'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/3630'

# Initialize Spotipy with authentication
auth_manager = SpotifyOAuth(scope="playlist-modify-public user-library-read user-read-recently-played user-top-read",
                             open_browser=False)

spotify = spotipy.Spotify(auth_manager=auth_manager)

st.title("SpotiMix: Your Playlist Maker")
st.markdown(
        """
            Welcome to the Spotify Playlist Recommendation System! 🎵

            This app is your gateway to creating personalized Spotify playlists based on your favorite artists. Whether you have a particular artist in mind or are looking for recommendations, we've got you covered.

            To get started, simply enter an artist's name in the input field below and explore a world of musical possibilities. We'll provide recommendations and let you craft the perfect playlist to match your mood.

            Let the music adventure begin! 🎶
        """
    )


# User selects their preferred artist
selected_artist = st.text_input("Enter the name of the artist:")

# Search for tracks by the selected artist
if selected_artist:
    artist_tracks = spotify.search(q=f"artist:{selected_artist}", type="track", limit=10)

    if artist_tracks:

        # Create a playlist with the tracks by the selected artist
        playlist_name = f"{selected_artist} Playlist"
        user_id = spotify.me()["id"]
        playlist = spotify.user_playlist_create(user=user_id, name=playlist_name, public=True)

        # Add the artist's tracks to the playlist
        track_uris = [track["uri"] for track in artist_tracks["tracks"]["items"]]
        spotify.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

        # Generate a Spotify link for the created playlist
        access_token = auth_manager.get_access_token()['access_token']
        spotify_link = f"https://open.spotify.com/playlist/{playlist['id']}?si={access_token}"

        st.success(f"Playlist '{playlist_name}' created with {len(track_uris)} tracks by {selected_artist}.")
        st.markdown(f"Access your playlist on [Spotify]({spotify_link}).")
    else:
        st.warning(f"No tracks found for the artist {selected_artist}. Please try a different artist.")
else:
    st.warning("Enter the name of an artist to create a playlist.")


