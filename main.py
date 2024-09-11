import requests
import os
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

Date = input("What year do you want to travel to?Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{Date}/")
data = response.text
soup = BeautifulSoup(data, "html.parser")
songs = []
list = soup.find_all(name= "h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
for every in range(0,9):
    songs.append(re.sub('\\s+', '', list[every].text))
songs.reverse()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    redirect_uri=os.getenv('redirect_uri'),
    scope='playlist-modify-public'
))

# Find Spotify track IDs
track_ids = []
for song in songs:
    result = sp.search(q=song, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_ids.append(track['id'])
        print(f"Found: {track['name']} by {track['artists'][0]['name']} (ID: {track['id']})")
    else:
        print(f"Track not found for song: {song}")

# Create a new playlist (or use an existing one)
user_id = sp.me()['id']
playlist_name = f'{Date}Billboard 100'
new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=f'Top songs from Billboard Hot 100 from the year {Date}')

# Add tracks to the playlist
if track_ids:
    sp.playlist_add_items(new_playlist['id'], track_ids)
    print(f"Tracks added to the playlist '{playlist_name}' (ID: {new_playlist['id']})")
else:
    print("No tracks to add to the playlist.")

