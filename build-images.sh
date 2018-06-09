#!/usr/bin/env bash

cd ./web-frontend/
docker build -t web-frontend .
docker tag web-frontend austinv11/discord4j:web-frontend
docker push austinv11/discord4j:web-frontend

cd ../nginx/
docker build -t nginx .
docker tag nginx austinv11/discord4j:nginx
docker push austinv11/discord4j:nginx

cd ../database/
docker build -t database .
docker tag database austinv11/discord4j:database
docker push austinv11/discord4j:database