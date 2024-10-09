import requests

SPOTIFY_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

def get_spotify_access_token(client_id:str, client_secret:str) -> str | None:
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    response = requests.post(SPOTIFY_TOKEN_ENDPOINT, headers=headers, data=data)

    if response.status_code != 200:
        print(response.content)
        return None

    json_response = response.json()
    access_token = json_response.get('access_token')
    
    return access_token