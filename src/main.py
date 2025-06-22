from spotify.auth import get_spotify_client
from spotify.service import SpotifyService
from datastore import DataStore
from spotify.spotify_data_manager import SpotifyDataManager
from pprint import pprint

client = get_spotify_client("yash")
spotify = SpotifyService(client)
store = DataStore("yash")
data_manager = SpotifyDataManager(spotify, store)

saved_tracks = data_manager.get_saved_tracks()
playlists = data_manager.get_playlists()

tracks_in_playlist = set()
for playlist in playlists:
    if playlist.tracks:
        for track in playlist.tracks:
            tracks_in_playlist.add(track.id)

orphan_tracks = [track for track in saved_tracks
                if track.id not in tracks_in_playlist]
orphan_track_names = [track.name for track in orphan_tracks]
pprint(orphan_track_names)
print(len(orphan_track_names))