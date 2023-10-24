import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import os


# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'f315c6bace724974b42a5b2477423a23'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'e6917aeeb4e946e1a0a5a372a6e51af9'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/8080'

# Sets up authentication and scope.
auth_manager = SpotifyOAuth(scope="user-library-read playlist-modify-public", 
                            open_browser=False)

auth_manager.get_authorize_url()


import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotipy with your authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", open_browser=False))

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
    return playlist

def add_tracks_to_playlist(playlist_id, track_uris):
    sp.playlist_add_items(playlist_id, track_uris)

# Get recommendations for a track
track_name = "Your Track Name"
track_uri = get_track_uri(track_name)

if track_uri:
    # Create a playlist
    playlist_name = "Recommended Playlist"
    playlist = create_playlist(playlist_name)

    # Get recommended tracks based on the selected track
    recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']

    # Extract track URIs from recommendations
    track_uris = [track['uri'] for track in recommendations]

    # Add recommended tracks to the playlist
    add_tracks_to_playlist(playlist['id'], track_uris)

    print(f"Playlist '{playlist_name}' created with {len(track_uris)} recommended tracks.")
