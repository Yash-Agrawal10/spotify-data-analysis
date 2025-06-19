from spotify.auth import get_spotify_client
from spotify.service import SpotifyService
from datastore import DataStore
from spotify_data_manager import SpotifyDataManager

client = get_spotify_client("yash")
spotify = SpotifyService(client)
store = DataStore("yash")
data_manager = SpotifyDataManager(spotify, store)

liked_songs = data_manager.get_saved_tracks()
print(liked_songs[0].model_dump_json(indent=2))

playlists = data_manager.get_playlists()
print(playlists[0].model_dump_json(indent=2))

playlist_tracks = data_manager.get_playlist_tracks(playlists[0])
print(playlist_tracks[0].model_dump_json(indent=2))