#!/usr/bin/env python3

import os
from tempfile import TemporaryDirectory

import click
from PIL import Image
from bottle import route, run, request, BaseRequest, HTTPError, default_app
from moviepy.video.io.VideoFileClip import VideoFileClip
from telegram import Bot
from telegram.utils.request import Request

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100

global BOT_TOKEN, CHAT_ID


req = Request()
# req = Request(proxy_url='socks5h://',
#               urllib3_proxy_kwargs={'username': '', 'password': ''})


@route('/', method='POST')
def index():
    bot = Bot(BOT_TOKEN, request=req)

    if 'filename' not in request.params:
        raise HTTPError(400, 'filename param is missing')
    filename = os.path.basename(request.params['filename'])

    with TemporaryDirectory() as d:
        fpath = os.path.join(d, filename)
        with open(fpath, 'wb') as f:
            body = request.body
            while True:
                chunk = body.read(0xFFFF)
                if not chunk:
                    break
                f.write(chunk)
        if filename.endswith('.jpg'):
            bot.send_photo(CHAT_ID, open(fpath, 'rb'))
        else:
            thumb = os.path.join(d, 'thumb.jpg')
            clip = VideoFileClip(fpath)
            frame = clip.get_frame(t=1)
            im = Image.fromarray(frame)
            im.thumbnail((320, 320), Image.ANTIALIAS)
            im.save(thumb)
            bot.send_video(CHAT_ID, open(fpath, 'rb'), clip.duration,
                           width=clip.size[0], height=clip.size[1], supports_streaming=True,
                           thumb=open(thumb, 'rb'))
    return 'OK'


@click.command()
@click.option('--host', '-h', envvar='HOST', default='0.0.0.0', type=str)
@click.option('--port', '-p', envvar='PORT', default=8080, type=int)
@click.option('--token', '-t', envvar='BOT_TOKEN', type=str)
@click.option('--chat', '-c', envvar='CHAT_ID', type=str)
def start(host, port, token, chat):
    global BOT_TOKEN, CHAT_ID
    BOT_TOKEN = token
    CHAT_ID = chat
    run(host=host, port=port)


if __name__ == '__main__':
    start()

app = default_app()
