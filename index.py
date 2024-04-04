from flask import Flask, request, redirect, Response
from http import HTTPStatus
import re
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_request():
    url = request.url
    parsed_url = urlparse(url)
    path = parsed_url.path

    if path.startswith('/channel/'):
        channel = path.split('/')[2].split('.')[0]

        if channel:
            youtube_url = f'https://www.youtube.com/channel/{channel}/live'
            response = requests.get(youtube_url, headers={'Cache-Control': 'max-age=0'})

            if response.ok:
                text = response.text
                stream = re.search(r'(?<=hlsManifestUrl":").*\.m3u8', text)

                if stream:
                    return redirect(stream.group(0), code=HTTPStatus.FOUND)
                else:
                    raise ValueError('HLS manifest URL not found')
            else:
                raise ValueError(f'Youtube URL ({youtube_url}) failed with status: {response.status_code}')
        else:
            raise ValueError(f'Channel ID not found in URL: {url}')
    else:
        raise ValueError(f'Path not found: {path}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
