import re
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
