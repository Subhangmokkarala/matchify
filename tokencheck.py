import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = os.getenv('SCOPE')

# Function to get Spotify token
def get_spotify_token():
    # Create an instance of the SpotifyOAuth class with your credentials
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    
    # Prompt the user to log in to Spotify and authorize the app
    token_info = sp_oauth.get_access_token()
    
    # Extract the access token
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")

    return token_info
def validate_token(token_info):
    if not token_info or 'access_token' not in token_info:
        return False
    # You could also add more checks if needed
    return True

# If run as a script, call the function and return the token
if __name__ == "__main__":
    token_info = get_spotify_token()
