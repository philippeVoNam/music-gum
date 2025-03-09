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
disp.clear()
image = Image.open("example.png")
image = image.resize((150, 150))
image = image.rotate(-90)

masterImage = Image.new("RGB", (disp.width,disp.height), (255, 250, 225))

infoImage = Image.new("RGB", (150, 150), (255, 250, 225))
draw = ImageDraw.Draw(infoImage)
Font1 = ImageFont.truetype("Font/Roboto-Regular.ttf", 10.5)

masterImage.paste(image, (10,10))

name = current_track["item"]["name"]
name = name[:15] # fit on the screen
volume = str(current_track["device"]["volume_percent"])
draw.text((15, 50), name, fill = (105, 103, 97), font=Font1)
draw.text((130, 50), volume, fill = (105, 103, 97), font=Font1)
draw.rectangle((15, 70, 142, 80), fill = (237, 232, 209), width = 1)
infoImage = infoImage.rotate(-90)
draw = ImageDraw.Draw(infoImage)

while True:
    current_track = sp.current_playback()
    percentComplete = int(current_track["progress_ms"] / current_track["item"]["duration_ms"] * 100)
    progress = str(round(current_track["progress_ms"]/1000, 2))
    a = 70
    b = 15
    c = 80
    d = 15 + (percentComplete * 142 / 100)
    draw.rectangle((a, b, c, d), fill = (105, 103, 97), width = 1)
    masterImage.paste(infoImage, (0,160))

    #draw.text((10, 240), progress, fill = (105, 103, 97), font=Font1)
    disp.ShowImage(masterImage, 0, 0)
    time.sleep(0.1)

disp.module_exit()
