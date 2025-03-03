import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

load_dotenv()

ID = os.getenv("id")
SECRET = os.getenv("secret")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,
                                               client_secret=SECRET,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read"))

cmd = ""
while cmd != "q":
    cmd = input("cmd : ")
    if cmd == "l":
        sp.next_track()
    elif cmd == "h":
        sp.previous_track()
    elif cmd == "p":
        current_track = sp.current_playback()
        pprint(current_track["item"]["name"])
