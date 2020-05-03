import os

from flask import Flask, jsonify
from flask_caching import Cache
from flask_cors import CORS
from github import Github

config = {
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
CORS(app, origins='*')
app.config.from_mapping(config)
cache = Cache(app)

github = Github(os.environ.get('ACCESS_TOKEN'))


@app.route("/versions", methods=["GET"])
@cache.cached(timeout=3*60*60)  # 3 hours in seconds
def handle():
    repo = github.get_repo("Discord4J/Discord4J")
    releases = list()
    for release in repo.get_releases().get_page(0):  # It's a paginated api, so lets use just the first page
        releases.append({
            "tag": release.tag_name,
            "title": release.title,
            "prerelease": release.prerelease,
            "url": release.url
        })

    return jsonify(releases)


@app.route("/")
def home():
    return "Hello World"


if __name__ == '__main__':
    app.run('0.0.0.0')
