import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

#importing spotipy module among others
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
URL_REDIRECT = "http://example.com"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret= CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
#authentication for the client ID and Secret, env variables
user_id = sp.current_user()["id"]


year = input("What year will we travel to? (YYYY-MM-DD)\n")
url = f"https://www.billboard.com/charts/hot-100/{year}/"
response = requests.get(url)
response.raise_for_status()
web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")
song_titles = soup.select("li ul li h3")
#scraping the billboard top 100 of the year
title_list = []
for title in song_titles:
    temp_title = title.get_text().replace("\n", " ")
    temp_title_two = temp_title.replace("\t", " ").strip()
    title_list.append(temp_title_two)

print(title_list)
song_uris = []
for title in title_list:
    results = sp.search(q=f"track:{title} year:{year}", type="track") #searching results for that year
    song_uris.append(results["tracks"]["items"][0]["uri"])
print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
#appending the playlist with my searches
