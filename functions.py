import base64, requests

from io import BytesIO
from jinja2 import Template

def generate_image_base64(image_path: str) -> str:
    with open(image_path, 'rb') as image_buffer:
        image_content = image_buffer.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        return image_base64
    
def get_image_from_url(url: str) -> str | None:
    response = requests.get(url)

    if response.status_code != 200:
        print(response.content)
        return None

    img_buffer = BytesIO(response.content)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return img_base64

def load_template(template_path: str) -> Template:
    with open(template_path, 'r', encoding='utf-8') as file:
        return Template(file.read())
    
def generate_track_duration(duration_ms: str) -> str:
    track_duration_seconds = duration_ms // 1000
    minutes = track_duration_seconds // 60
    seconds = track_duration_seconds % 60
    return f'{minutes}:{str(seconds).zfill(2)}'