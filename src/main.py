from spotify_auth import get_spotify_client
from spotify_service import SpotifyService

client = get_spotify_client("yash")
service = SpotifyService(client)

liked_songs = service.get_saved_tracks()
print(liked_songs[0].model_dump_json(indent=2))

playlists = service.get_playlists()
print(playlists[0].model_dump_json(indent=2))

playlist_tracks = service.get_playlist_tracks(playlists[0])
print(playlist_tracks[0].model_dump_json(indent=2))