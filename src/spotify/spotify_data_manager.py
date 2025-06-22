from spotify.service import SpotifyService
from spotify.models import SpotifyPlaylist, SpotifyTrack, SpotifyAlbum
from datastore import DataStore

class SpotifyDataManager:

    def __init__(self, spotify: SpotifyService, store: DataStore):
        self._spotify = spotify
        self._store = store
    
    def get_saved_tracks(self, use_cached=True, key="saved-tracks") -> list[SpotifyTrack]:
        if use_cached:
            cached = self._store.load(key)
            if cached:
                return [SpotifyTrack(**item) for item in cached]
        tracks = self._spotify.get_saved_tracks()
        self._store.save(key, [track.model_dump(mode='json') for track in tracks])
        return tracks

    def get_saved_albums(self, use_cached=True, key="saved-albums") -> list[SpotifyAlbum]:
        if use_cached:
            cached = self._store.load(key)
            if cached:
                return [SpotifyAlbum(**item) for item in cached]
        albums = self._spotify.get_saved_albums()
        self._store.save(key, [album.model_dump(mode='json') for album in albums])
        return albums

    def get_playlist_names_and_ids(self, use_cached=True, key="playlist-names-and-ids") -> list[SpotifyPlaylist]:
        if use_cached:
            cached = self._store.load(key)
            if cached:
                return [SpotifyPlaylist(**item) for item in cached]
        playlists = self._spotify.get_playlist_names_and_ids()
        self._store.save(key, [playlist.model_dump(mode='json') for playlist in playlists])
        return playlists

    def get_playlist_tracks(self, playlist: SpotifyPlaylist, use_cached=True, key="") -> SpotifyPlaylist:
        if key == "":
            key = f"playlist-{playlist.name}-{playlist.id}"
        if use_cached:
            cached = self._store.load(key)
            if cached:
                return SpotifyPlaylist(**cached)
        playlist = self._spotify.get_playlist_tracks(playlist)
        self._store.save(key, playlist.model_dump())
        return playlist