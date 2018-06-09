import functools
import json
import os
import platform
from collections import namedtuple
from typing import List, Tuple, Dict, Set, Any
import re

from flask import Flask, request, abort
# from gevent.pywsgi import WSGIServer
import yaml
import requests

Service = namedtuple('Service', ['name', 'image', 'requires'])

app = Flask('Docker webhook')
app.debug = os.environ.get('DEBUG') == 'true'


SERVICE_NAME = 'webhook'  # We need to be careful when updating ourselves!


HOST_ADDRESS = None
# From: https://stackoverflow.com/a/33197361
IP_REGEX = re.compile(r'(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')


@app.route("/ping", methods=['POST'])
def ping():
    global HOST_ADDRESS

    if HOST_ADDRESS is not None:  # Only collect once!
        print("Ping attempted despite having an established address!", flush=True)
        abort(404)
    else:
        matches = IP_REGEX.findall(request.remote_addr)
        if len(matches) > 0:
            HOST_ADDRESS = matches[0]
        else:
            print("Unable to parse ip from %s!" % request.remote_addr, flush=True)
            abort(500)
        print("Using pinged address:", flush=True)
        print(HOST_ADDRESS, flush=True)
        print("Confirming configuration...", flush=True)
        status_code = None
        try:
            status_code = requests.get(HOST_ADDRESS + "/docker", params={'container': get_container_info()}).status_code
        except:
            pass
        if status_code == 200:
            return "OK"
        else:
            print("Invalid confirmation! Forgetting address...", flush=True)
            HOST_ADDRESS = None
            abort(403)


def signal_self_update():
    print("Signalling for a webhook container update...", flush=True)
    requests.post(HOST_ADDRESS + "/docker", json={'container': get_container_info(), 'op': 'self_update'})


def call(cmd):
    print("Signalling for command execution...", flush=True)
    requests.post(HOST_ADDRESS + "/docker", json={'container': get_container_info(), 'op': 'cmd', 'payload': cmd})


@app.route("/docker", methods=['GET', 'POST'])
def docker():
    if request.method == 'GET':
        return "Yes, I am alive"
    elif request.method == 'POST':
        payload = json.loads(request.data)
        tag = payload['push_data']['tag']
        repo_name = payload['repository']['repo_name']
        formatted_name = "%s:%s" % (repo_name, tag)
        print("Update detected for %s" % formatted_name, flush=True)
        services, old_raw_services = read_services()
        raw_services = old_raw_services
        target = None
        mark_for_rebuild = False
        while True:
            for service in services:
                if service.image == formatted_name:
                    target = service
                    break
            if target is None and not mark_for_rebuild:
                mark_for_rebuild = True
                update_repo()
                services, raw_services = read_services()
            if target is None and mark_for_rebuild:
                abort(501)
                print("Unused image was pushed! Are you sure the docker-compose.yml is up to date?", flush=True)
                return
            else:
                break
        if raw_services == old_raw_services:
            print("Single image update...", flush=True)
            if target.name == SERVICE_NAME:
                signal_self_update()
            else:
                update_services(frozenset(target), frozenset(), frozenset(), services)
        else:
            print("docker-compose.yml update...", flush=True)
            update_self = False
            if target.name == SERVICE_NAME:
                update_self = True
                changed_services = set()
            else:
                changed_services = set(target)
            added_services = set()
            removed_services = set()
            docker_compose_updated = False
            for service_name, service in raw_services['services']:
                if service_name == SERVICE_NAME:
                    update_self = True
                    continue
                if service_name not in old_raw_services['services']:
                    added_services.add(service)
                elif service != old_raw_services['services'][service_name]:
                    changed_services.add(service)
            for service_name, service in old_raw_services['services']:
                if service_name == SERVICE_NAME:
                    update_self = True
                    continue
                if service_name not in raw_services['services']:
                    removed_services.add(service_name)
            for key, value in raw_services:
                if docker_compose_updated:
                    break
                if key == 'services':
                    continue
                if key not in raw_services or value != old_raw_services[key]:
                    docker_compose_updated = True
            for key, value in old_raw_services:
                if docker_compose_updated:
                    break
                if key not in raw_services:
                    docker_compose_updated = True
            update_services(changed_services, added_services, removed_services, services)
            if docker_compose_updated:
                update_cluster()
            if update_self:
                signal_self_update()
        return "OK"
    abort(403)


def read_services() -> Tuple[List[Service], Dict[str, Any]]:
    with open("./docker-compose.yml", 'r') as f:
        yml = yaml.load(f)

    services = []
    raw_services: Dict[str, Any] = yml
    for service_name, service in yml['services'].items():
        services.append(Service(service_name, service['image'], [] if "depends_on" not in service else service['depends_on']))
    return services, raw_services


def update_repo():
    print("Updating the local meta repo clone...", flush=True)
    call("git fetch --all")
    call("git reset --hard origin/master")


def update_services(changed_services: Set[Service], added_services: Set[Service], removed_services: Set[Service], all_services: List[Service]):
    @functools.lru_cache(maxsize=64)
    def get_dependents(service: Service) -> Set[Service]:
        deps = set()
        for dep in all_services:
            if service.name in dep.requires:
                deps.add(dep)
                deps |= get_dependents(dep)
        return deps

    updated_services = set()

    def update_all(services, installed_services):
        global SERVICE_NAME
        for s in services:
            if s not in installed_services:
                deps = get_dependents(s)
                for dep in deps:
                    call("docker-compose pause %s" % dep.name)
                call("docker-compose up -d --no-deps --force-recreate %s" % s.name)
                for dep in deps:
                    call("docker-compose unpause %s" % dep.name)
                installed_services.add(s)
        return installed_services

    print("Updating %s services..." % str(len(changed_services) + len(added_services) + len(removed_services)), flush=True)
    updated_services = update_all(changed_services, updated_services)
    update_all(added_services, updated_services)
    for removed in removed_services:
        call("docker-compose rm -f -s -v %s" % removed.name)


def update_cluster():  # TODO: Do rolling updates instead somehow
    print("Updating the local cluster...", flush=True)
    call("docker-compose up -d --remove-orphans")


def get_container_info():
    container_hash = platform.node()
    assert len(container_hash) != 0
    return container_hash


if __name__ == '__main__':
    pass
    # app.run(host='0.0.0.0', port=2314)
    # http_server = WSGIServer(('', 2314), app)
    # http_server.serve_forever()
