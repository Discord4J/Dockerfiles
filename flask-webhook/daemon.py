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
    print("Verifying access for container hash %s..." % container, flush=True)
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

    verified = specified_image is not None and specified_image.container == 'dockerfiles_%s_1' % SERVICE_NAME
    if not verified:
        print("Verification failed!", flush=True)
    else:
        print("Verified!", flush=True)
    return verified


@app.route("/docker", methods=['GET', 'POST'])
def docker():
    if IN_CONTAINER:
        print("Cannot access the daemon inside of a container!", flush=True)
        abort(500)

    if request.method == 'GET':
        print("We are getting pinged...", flush=True)
        if 'container' in request.args:
            if verify_container(request.args.get('container')):
                return "OK"
        abort(403)
    elif request.method == 'POST':
        print("Operation requested...", flush=True)
        req = json.loads(request.data)
        if verify_container(req.get('container', default='nothing')):
            op = req['op']
            if op == 'self_update':
                print("Updating the webhook container...", flush=True)
                call("docker-compose up -d --no-deps --force-recreate %s" % SERVICE_NAME, shell=True)
                print("Pinging webhook container...", flush=True)
                requests.post("http://127.0.0.1:2314/ping")
                return "OK"
            elif op == 'cmd':
                print("Executing arbitrary command...", flush=True)
                payload = req['payload']
                print("> %s" % payload, flush=True)
                call(payload, shell=True)
                return "OK"
        print("Could not verify the authenticity of the caller, aborting...", flush=True)
        abort(403)


if __name__ == "__main__":
    # http_server = WSGIServer(('', 1337), app)
    # http_server.start()
    print("Pinging webhook container...", flush=True)
    requests.post("http://127.0.0.1:2314/ping")
    # http_server.serve_forever()
