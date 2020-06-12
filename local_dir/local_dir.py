#!/usr/bin/env python3

import os

import click
from bottle import route, run, request, BaseRequest, HTTPError, default_app

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100


global OUTPUT_DIRECTORY


@route('/', method='POST')
def index():
    if 'filename' not in request.params:
        raise HTTPError(400, 'filename param is missing')
    filename = os.path.basename(request.params['filename'])

    fpath = os.path.join(OUTPUT_DIRECTORY, filename)
    with open(fpath, 'wb') as f:
        body = request.body
        while True:
            chunk = body.read(0xFFFF)
            if not chunk:
                break
            f.write(chunk)

    return 'OK'


@click.command()
@click.option('--host', '-h', envvar='HOST', default='0.0.0.0', type=str)
@click.option('--port', '-p', envvar='PORT', default=8080, type=int)
@click.option('--output', '-o', envvar='OUTPUT_DIR', default='output',
              type=click.Path(file_okay=False, writable=True, resolve_path=True))
def start(host, port, output):
    global OUTPUT_DIRECTORY
    OUTPUT_DIRECTORY = output
    os.makedirs(output, exist_ok=True)
    run(host=host, port=port)


if __name__ == '__main__':
    start()

app = default_app()
