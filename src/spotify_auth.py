import os
from spotipy import Spotify
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path

# Get .env values
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
data_dir = os.getenv("DATA_DIR")

def get_spotify_client(username: str, scope: str = "user-library-read") -> Spotify:
    # Create and validate cache path
    data_path = Path(str(data_dir))
    token_path = data_path / username / "spotify-token.cache"
    token_path.parent.mkdir(parents=True, exist_ok=True)

    # Authenticate
    auth_manager=SpotifyOAuth(
        client_id=client_id, 
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=str(token_path)
    )

    sp_client = Spotify(auth_manager=auth_manager)

    return sp_client