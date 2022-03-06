from os import getcwd
from os import path
from os import sep

from fastapi import FastAPI
from fastapi import Header
from fastapi.responses import Response
from fastapi.responses import HTMLResponse

app = FastAPI()

CHUNK_SIZE = 1024*1024  # 1 Megabyte
VIDEOS_DIR = f'{getcwd()}{sep}public{sep}videos{sep}'

@app.get('/')
async def index():
    with open('index.html') as f:
        content = f.read()
        return HTMLResponse(content=content, status_code=200)

@app.get('/videos/{name}')
async def get_video(name: str, range: str = Header(None)):
    # Getting video chunks range by "bytes-0-" pattern
    start, end = range.replace('bytes=', '').split('-')
    start = int(start)
    end = int(start + CHUNK_SIZE)

    video_path = f'{VIDEOS_DIR}{name}'
    video_size = path.getsize(video_path)

    with open(video_path, 'rb') as f:
        f.seek(start) # Go to specific file point
        content = f.read(end - start)

        headers = {
            'Content-Range': f'bytes {start}-{end}/{video_size}',
            'Accept-Ranges': 'bytes'
        }

        return Response(content=content, status_code=206, headers=headers, media_type='video/mp4')
