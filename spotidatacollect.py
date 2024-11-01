import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

def spotify_login():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope='user-top-read user-read-private'
    )
    auth_url = sp_oauth.get_authorize_url()
    return sp_oauth, auth_url

def get_spotify_data(code):
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI')
    )
    token_info = sp_oauth.get_access_token(code)
    
    if not token_info:
        raise ValueError("Invalid token information")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_data = sp.current_user()
    top_artists = sp.current_user_top_artists(limit=5)
    top_tracks = sp.current_user_top_tracks(limit=5)
    
    return {
        'id': user_data['id'],
        'top_artists': [artist['name'] for artist in top_artists['items']],
        'top_tracks': [track['name'] for track in top_tracks['items']]
    }
