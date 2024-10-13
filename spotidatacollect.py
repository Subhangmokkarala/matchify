# spotidatacollect.py
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Function to handle Spotify OAuth (Login)
def spotify_login(client_id, client_secret, redirect_uri, scope):
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()
    return sp_oauth, auth_url

# Function to get access token using the authorization code
def get_token(sp_oauth, code):
    token_info = sp_oauth.get_access_token(code)
    return token_info

# Function to fetch current user data
def get_user_data(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_data = sp.current_user()
    return user_data

# Function to fetch user's top artists
def get_top_artists(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=10)['items']
    return top_artists

# Function to fetch user's top tracks
def get_top_tracks(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=10)['items']
    return top_tracks
