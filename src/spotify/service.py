from spotipy import Spotify
from models import Track, SimplifiedPlaylist

class SpotifyService:

    def __init__(self, client: Spotify):
        self._client = client

    def _get_all(self, get_response, limit: int=50) -> list[dict]:
        items = []
        offset = 0
        while True:
            response = get_response(limit=limit, offset=offset)
            if not response:
                break
            batch = response["items"]
            if not batch:
                break
            items.extend(batch)
            offset += limit
        return items
    
    def get_saved_tracks(self) -> list[Track]:
        items = self._get_all(self._client.current_user_saved_tracks)
        tracks = [Track(**item["track"]) 
                  for item in items if item.get("track")]
        return tracks
    
    def get_playlists(self) -> list[SimplifiedPlaylist]:
        items = self._get_all(self._client.current_user_playlists)
        playlists = [SimplifiedPlaylist(**item) for item in items]
        return playlists

    def get_playlist_tracks(self, playlist: SimplifiedPlaylist) -> list[Track]:
        playlist_id = playlist.id
        items = self._get_all(
            lambda limit, offset: self._client.playlist_items(
                playlist_id, 
                limit=limit,
                offset=offset
            ),
            limit=100
        )
        playlist_tracks = [Track(**item["track"]) 
                           for item in items if item.get("track")]
        return playlist_tracks