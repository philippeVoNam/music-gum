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
from lib import LCD_1inch9
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
images = current_track["item"]["album"]["images"]
download_image(images[0]["url"], "example.png")


# LCD
# Raspberry Pi pin configuration:
disp = LCD_1inch9.LCD_1inch9()
disp.Init()
disp.bl_DutyCycle(100)
cmd = ""
while cmd != "q":
    size = input("size : ")
    x = int(input("x : "))
    y = int(input("y : "))
    cmd = input("cmd : ")
    disp.clear()
    image = Image.open("example.png")
    image = image.resize((170, int(size)))
    image = image.rotate(270)
    disp.ShowImage(image, x, y)

while cmd != "q":
    size = input("size : ")
    a = int(input("a : "))
    b = int(input("b : "))
    c = int(input("c : "))
    d = int(input("d : "))
    cmd = input("cmd : ")
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)
    draw.rectangle((a, b, c, d), fill = "BLACK")

disp.module_exit()
