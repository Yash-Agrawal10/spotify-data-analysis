from spotify.service import SpotifyService
from spotify.models import SpotifyPlaylist, SpotifyTrack, SpotifyAlbum
from datastore import DataStore

class SpotifyDataManager:

    def __init__(self, spotify: SpotifyService, store: DataStore):
        self._spotify = spotify
        self._store = store

    def _get_data(self, key, get_data, to_serializable, from_serializable, use_cached):
        if use_cached:
            stored_data = self._store.load(key)
            if stored_data:
                return from_serializable(stored_data)
        data = get_data()
        self._store.save(key, to_serializable(data))
        return data
    
    def get_saved_tracks(self, use_cached=True) -> list[SpotifyTrack]:
        return self._get_data("saved-tracks", 
                              self._spotify.get_saved_tracks,
                              lambda tracks: [track.model_dump(mode='json') for track in tracks],
                              lambda items: [SpotifyTrack(**item) for item in items],
                              use_cached)

    def get_saved_albums(self, use_cached=True) -> list[SpotifyAlbum]:
        return self._get_data("saved-albums", 
                              self._spotify.get_saved_albums,
                              lambda albums: [album.model_dump(mode='json') for album in albums],
                              lambda items: [SpotifyAlbum(**item) for item in items],
                              use_cached)

    def get_playlist_names_and_ids(self, use_cached=True) -> list[SpotifyPlaylist]:
        return self._get_data("playlists", 
                              self._spotify.get_playlist_names_and_ids, 
                              lambda playlists: [playlist.model_dump(mode='json') for playlist in playlists],
                              lambda items: [SpotifyPlaylist(**item) for item in items],
                              use_cached)

    def get_playlist_tracks(self, playlist: SpotifyPlaylist, use_cached=True) -> SpotifyPlaylist:
        return self._get_data(f"playlist-{playlist.name}-{playlist.id}", 
                              lambda: self._spotify.get_playlist_tracks(playlist),
                              lambda playlist: playlist.model_dump(),
                              lambda item: SpotifyPlaylist(**item),
                              use_cached)