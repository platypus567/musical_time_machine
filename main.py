import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


year = input("What year will we travel to? (YYYY-MM-DD)\n")
url = f"https://www.billboard.com/charts/hot-100/{year}/"
response = requests.get(url)
response.raise_for_status()
web_data = response.text
soup = BeautifulSoup(web_data, "html.parser")
song_titles = soup.select("li ul li h3")
title_list = []
for title in song_titles:
    temp_title = title.get_text().replace("\n", " ")
    temp_title_two = temp_title.replace("\t", " ").strip()
    title_list.append(temp_title_two)

print(title_list)
#for item in title_list:
    #results = sp.search(q=item, limit=1)
  #  for idx, track in enumerate(results['tracks']['items']):
       # print(track['name'])
