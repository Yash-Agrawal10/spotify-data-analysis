from spotipy import Spotify
from typing import List, Dict, Any, Callable
from spotify_models import Track, Artist, Album, SimplifiedArtist

class SpotifyService:

    def __init__(self, client: Spotify):
        self._client = client

    def _get_all(self, get_batch, limit: int=50):
        items = []
        offset = 0
        while True:
            batch = get_batch(limit, offset)
            if not batch:
                break
            items.extend(batch)
            offset += limit
        return items
    
    def get_saved_tracks(self):
        items = self._get_all(
            lambda limit, offset: self._client.current_user_saved_tracks(limit=limit, offset=offset)["items"])