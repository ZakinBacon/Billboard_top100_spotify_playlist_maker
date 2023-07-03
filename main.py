from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

spotify_clientID = os.getenv("spotify_clientID")
spotify_client_secret = os.getenv("spotify_client_secret")
username = os.getenv("username")

song_uris = []

date = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
billboard_webpage = response.content

# Creating our Soup
soup = BeautifulSoup(billboard_webpage, "html.parser")


titles = soup.select("li ul li h3")
artists = soup.find_all(name="span", class_="u-max-width-330")

song_names = [song.getText().strip() for song in titles]
artists_name = [artist.getText().strip() for artist in artists]

print(f"titles: {song_names}\nArtists: {artists_name}")

artist_count = 0

# Used to authenticate
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_clientID,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=username,
    )
)

user_id = sp.current_user()["id"]
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"{song} {artists_name[artist_count]} ", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    artist_count += 1


print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description=f"Top 100 songs from {date}. Songs are listed in order.")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
