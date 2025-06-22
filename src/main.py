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

playlists_names_and_ids = data_manager.get_playlist_names_and_ids()
print(playlists_names_and_ids[-1].model_dump_json(indent=2))

playlist = data_manager.get_playlist_tracks(playlists_names_and_ids[-1])
if playlist.tracks != None:
    print(playlist.tracks[0])