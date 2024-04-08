from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("which year you want to travel to? Type the date in this format YYYY-MM-DD:")

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
                                client_id="95e79525a46e40629aa1cc90e4a27cf6",
                                client_secret="7ff264d9ee3b450fb47e2fe17f2fa60b",
                                redirect_uri="http://example.com",
                                scope="playlist-modify-private",
                                show_dialog=True,
                                cache_path=".cache"))

user_id = sp.current_user()["id"]

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
content = response.text
soup = BeautifulSoup(content, "html.parser")
name = soup.select(selector="li ul li h3")
song_name = [song.get_text().strip() for song in name]
print(song_name)

song_uris = []
year = date.split('-')[0]

for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri =  result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user="31x6v4ig6ythzz45ism3pcoxi3ri", name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
