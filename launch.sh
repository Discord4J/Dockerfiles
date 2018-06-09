#!/usr/bin/env bash
echo "Preparing services..."
docker-compose up -d
echo "Launching daemon hook..."
cd flask-webhook
source venv/bin/activate
pip install -r requirements.txt
gunicorn -b localhost:1337 daemon:app &
echo "Done!"