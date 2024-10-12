import requests, random, imgkit, json, platform
from io import BytesIO
from requests_oauthlib import OAuth1

from functions import generate_image_base64, get_image_from_url, load_template, generate_track_duration

def get_track_info(access_token: str, market: str, playlist_id: str) -> dict | None:
    playlist_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    params = {
        'market':market,
        'fields':'tracks.items(track(name, artists(name), album(name, images(url), release_date), explicit, popularity, href, external_urls, duration_ms))'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(playlist_endpoint, headers=headers, params=params)

    if response.status_code != 200:
        print(response.content)
        return None

    json_response = response.json()
    tracks = json_response.get('tracks')
    items = tracks.get('items')

    random_song_position = random.randint(0, len(items)-1)

    track = items[random_song_position]
    track = track.get('track')
    
    return track

def generate_image(track: dict, template_path: str, css_path: str, images_paths: dict) -> bytes:
    album_data = track.get('album')
    album_images = album_data.get('images')
    album_cover = album_images[0].get('url')
    album_cover_base64 = get_image_from_url(album_cover)
    logo_icon_base64 = generate_image_base64(images_paths.get('icon'))
    popularity_icon_base64 = generate_image_base64(images_paths.get('popularity'))
    spotify_icon_base64 = generate_image_base64(images_paths.get('spotify'))
    flower_icon_base64 = generate_image_base64(images_paths.get('flower'))

    track_name = track.get('name')
    track_artists = ', '.join(artist['name'] for artist in track.get('artists'))
    external_urls = track.get('external_urls')
    spotify_url = external_urls.get('spotify')
    album_data = track.get('album')
    album_name = album_data.get('name')
    album_images = album_data.get('images')
    track_album_release_date = album_data.get('release_date')
    track_is_explicit = track.get('explicit')
    track_popularity = track.get('popularity')
    track_duration = generate_track_duration(track.get('duration_ms'))

    html_content = load_template(template_path)
    rendered_template = html_content.render(
        track_name=track_name,
        track_album_release_year=track_album_release_date[0:4],
        track_artists=track_artists,
        album=album_name,
        duration=track_duration,
        popularity=track_popularity,
        explicit = 'E' if track_is_explicit is True else '',
        track_image=f'data:image/jpeg;base64,{album_cover_base64}',
        logo_icon=f'data:image/png;base64,{logo_icon_base64}',
        popularity_icon=f'data:image/png;base64,{popularity_icon_base64}',
        spotify_icon=f'data:image/png;base64,{spotify_icon_base64}',
        flower_icon=f'data:image/png;base64,{flower_icon_base64}',
    )

    img_buffer = BytesIO()
    img_buffer.seek(0)

    wkhtmltoimage_route = '/usr/local/bin/wkhtmltoimage' if platform.system() != 'Windows' else 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe'
    configuration = imgkit.config(wkhtmltoimage=wkhtmltoimage_route)
    options = {
        'format': 'png',
        'width':'1450',
        'no-stop-slow-scripts': '',
        'enable-local-file-access': '',
        'quiet': ''
    }
    imgkit.from_string(rendered_template, 'output.png', config=configuration, options=options)

    with open('output.png', 'rb') as temp_file:
        img_buffer.write(temp_file.read())        

    messages = [
        f'La canción del día es... ¡{track_name}!\n\nAquí la encuentras: {spotify_url}',
        f'{track_name}.\n\nEncuéntrala en: {spotify_url}',
        f'Con una popularidad de {track_popularity}, "{track_name}".\n\nCompruébalo tú mismx en: {spotify_url}',
        f'Escucha {track_name}, sólo dura {track_duration}.\n\nEscúchala en: {spotify_url}',
    ]

    random_message_position = random.randint(0, len(messages)-1)

    return img_buffer, f'{messages[random_message_position]}\n\n#Spotify'

def post_image(image:BytesIO, twitter_authorization:OAuth1, post_body: str) -> None:
    TWITTER_MEDIA_ENDPOINT = 'https://upload.twitter.com/1.1/media/upload.json'
    TWITTER_TWEET_ENDPOINT = 'https://api.twitter.com/2/tweets'

    files = {
        'media':image.getvalue(),
        'media_category':'tweet_image',
    }

    response = requests.post(TWITTER_MEDIA_ENDPOINT, auth=twitter_authorization, files=files)

    if not response.status_code == 200:
        print(response.content)
        return None
    
    json_tweet = response.json()

    headers = {
        'Content-Type':'application/json'
    }

    post_data = {
        'text':post_body,
        'media': {
            'media_ids': [json_tweet.get('media_id_string')]
        }
    }

    response = requests.post(TWITTER_TWEET_ENDPOINT, auth=twitter_authorization, headers=headers, data=json.dumps(post_data))

    if not response.status_code == 200:
        print(response.content)
        return None
    
    print(response.json())