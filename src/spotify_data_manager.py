from spotify.service import SpotifyService
from spotify.models import SimplifiedPlaylist
from datastore import DataStore

class SpotifyDataManager:

    def __init__(self, spotify: SpotifyService, store: DataStore):
        self._spotify = spotify
        self._store = store

    def _get_data(self, key, get_data, use_cached):
        if use_cached:
            stored_data = self._store.load(key)
            if stored_data:
                return stored_data
        data = get_data()
        self._store.save(key, data)
        return data
    
    def get_saved_tracks(self, use_cached=True):
        return self._get_data("saved-tracks", 
                              self._spotify.get_saved_tracks, 
                              use_cached)

    def get_playlists(self, use_cached=True):
        return self._get_data("playlists", 
                              self._spotify.get_playlists, 
                              use_cached)

    def get_playlist_tracks(self, playlist: SimplifiedPlaylist, use_cached=True):
        return self._get_data(f"playlist-{playlist.id}", 
                              lambda: self._spotify.get_playlist_tracks(playlist), 
                              use_cached)