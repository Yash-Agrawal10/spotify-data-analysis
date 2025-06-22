from spotify.auth import get_spotify_client
from spotify.service import SpotifyService
from datastore import DataStore
from spotify.spotify_data_manager import SpotifyDataManager

client = get_spotify_client("yash")
spotify = SpotifyService(client)
store = DataStore("yash")
data_manager = SpotifyDataManager(spotify, store)

saved_tracks = data_manager.get_saved_tracks()

saved_albums = data_manager.get_saved_albums()

playlists_names_and_ids = data_manager.get_playlist_names_and_ids()

playlist = data_manager.get_playlist_tracks(playlists_names_and_ids[-1])