import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import lyricsgenius
from config.settings import API_KEYS

# Test Spotify
try:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=API_KEYS['spotify_client_id'],
        client_secret=API_KEYS['spotify_client_secret']
    ))
    results = spotify.search(q='test song', type='track', limit=1)
    print("Spotify API: OK")
except Exception as e:
    print(f"Spotify API Error: {e}")

# Test YouTube
try:
    youtube = build('youtube', 'v3', developerKey=API_KEYS['youtube_api_key'])
    request = youtube.search().list(q='test song', part='snippet', maxResults=1)
    response = request.execute()
    print("YouTube API: OK")
except Exception as e:
    print(f"YouTube API Error: {e}")

# Test Genius (lyrics)
try:
    genius = lyricsgenius.Genius()  # No key needed
    song = genius.search_song('test song')
    print("Genius API: OK")
except Exception as e:
    print(f"Genius API Error: {e}")

print("API tests completed.")
