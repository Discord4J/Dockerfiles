import os
from collections import namedtuple
from subprocess import call, Popen, PIPE

import requests
from flask import Flask, request, abort
import json

# from gevent.pywsgi import WSGIServer

"""
Listens on port 1337 for POST commands to allow for arbitrary shell command execution from docker containers.
This is a security risk! Ensure that this port is NOT exposed to the world.
"""

app = Flask('Docker webhook daemon')
app.debug = os.environ.get('DEBUG') == 'true'

IN_CONTAINER = os.getenv('CONTAINER_STAT', 'no') == 'yes'
SERVICE_NAME = 'webhook'  # We need to be careful when updating ourselves!

Image = namedtuple('Image', ['container', 'repository', 'tag', 'image_id', 'size'])


def verify_container(container):
    cmd = Popen('docker-compose images', shell=True, stdout=PIPE)
    images_string, cmd_err = cmd.communicate()
    cmd.kill()

    images = set()
    for line in images_string.splitlines():
        split = line.split()
        images.add(Image(split[0], split[1], split[2], split[3], split[4] + split[5]))

    specified_image = None
    for image in images:
        if container == image.image_id:
            specified_image = image
            break

    return specified_image is not None and specified_image.container == 'dockerfiles_%s_1' % SERVICE_NAME


@app.route("/docker", methods=['GET', 'POST'])
def docker():
    if IN_CONTAINER:
        abort(500)

    if request.method == 'GET':
        if 'container' in request.args:
            if verify_container(request.args.get('container')):
                return "OK"
        abort(403)
    elif request.method == 'POST':
        req = json.loads(request.data)
        if verify_container(req.get('container', default='nothing')):
            op = req['op']
            if op == 'self_update':
                call("docker-compose up -d --no-deps --force-recreate %s" % SERVICE_NAME, shell=True)
                return "OK"
            elif op == 'cmd':
                payload = req['payload']
                call(payload, shell=True)
                return "OK"
        abort(403)


if __name__ == "__main__":
    # http_server = WSGIServer(('', 1337), app)
    # http_server.start()
    requests.post("http://127.0.0.1:2314/ping")
    # http_server.serve_forever()
