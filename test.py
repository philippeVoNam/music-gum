import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import requests

import os
import sys 
import time
import logging
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont

def download_image(url, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully: {file_name}")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

load_dotenv()

ID = os.getenv("id")
SECRET = os.getenv("secret")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,
                                               client_secret=SECRET,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read"))

current_track = sp.current_playback()
pprint(current_track["item"]["name"])
percentComplete = int(current_track["progress_ms"] / current_track["item"]["duration_ms"] * 100)
print(percentComplete)
# images = current_track["item"]["album"]["images"]
# download_image(images[0]["url"], "example.png")
