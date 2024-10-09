import os

from dotenv import load_dotenv
from requests_oauthlib import OAuth1
from datetime import datetime

from login import get_spotify_access_token
from bot import get_track_info, generate_image, post_image

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'assets', 'templates', 'template.html')
CSS_PATH = os.path.join(PROJECT_ROOT, 'assets', 'css', 'main.css')
IMAGES_PATHS = {
    "icon": os.path.join(PROJECT_ROOT, 'assets', 'img', 'icon.png'),
    "popularity": os.path.join(PROJECT_ROOT, 'assets', 'img', 'popularity.png'),
    "spotify": os.path.join(PROJECT_ROOT, 'assets', 'img', 'spotify.png'),
    "flower": os.path.join(PROJECT_ROOT, 'assets', 'img', 'flower.png'),
}

# Spotify settings
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
playlist_id = os.getenv('PLAYLIST_ID')
market = os.getenv('MARKET')

# Twitter keys
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_KEY_SECRET = os.getenv('ACCESS_KEY_SECRET')

if not all([client_id, client_secret, playlist_id, market]):
    raise ValueError('Not all environment variables are declared')

spotify_access_token = get_spotify_access_token(client_id, client_secret)

if not spotify_access_token:
    raise ValueError('There was a problem retrieving the access token')

track_info = get_track_info(spotify_access_token, market, playlist_id)

if not track_info:
    raise ValueError('There was a problem retrieving track\'s data') 

image, post_body = generate_image(track_info, TEMPLATE_PATH, CSS_PATH, IMAGES_PATHS)

if not image or not post_body:
    raise ValueError('There was a problem generating the image')

twitter_authorization = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET)

post_image(image, twitter_authorization, post_body)

os.remove('output.png')

print(f'Image posted succesfully, time: {datetime.now()}')