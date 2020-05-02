import os

from flask import Flask, jsonify
from github import Github

app = Flask(__name__)

github = Github(os.environ.get('ACCESS_TOKEN'))


@app.route("/versions", methods=["GET"])
def handle():
    repo = github.get_repo("Discord4J/Discord4J")
    releases = dict()
    for release in repo.get_releases():
        releases[release.tag_name] = {
            "title": release.title,
            "prerelease": release.prerelease,
            "url": release.url
        }

    return jsonify(reversed(releases))
