from spotipy import Spotify
from .models import SpotifyTrack, SpotifyPlaylist

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
    
    def get_saved_tracks(self) -> list[SpotifyTrack]:
        items = self._get_all(self._client.current_user_saved_tracks)
        print(items[0]["track"])
        tracks = [SpotifyTrack(**item["track"])
                  for item in items if item.get("track")]
        return tracks
    
    def get_playlist_names_and_ids(self) -> list[SpotifyPlaylist]:
        items = self._get_all(self._client.current_user_playlists)
        playlists = []
        for item in items:
            del item["tracks"]
        playlists = [SpotifyPlaylist(**item) for item in items]
        return playlists

    def get_playlist_tracks(self, playlist: SpotifyPlaylist) -> SpotifyPlaylist:
        items = self._get_all(
            lambda limit, offset: self._client.playlist_items(
                playlist.id, 
                limit=limit,
                offset=offset
            ),
            limit=100
        )
        playlist_tracks = [SpotifyTrack(**item["track"]) 
                           for item in items if item.get("track")]
        return SpotifyPlaylist(id=playlist.id, name=playlist.name, tracks=playlist_tracks)