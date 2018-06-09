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

cd ../confluence/
docker build -t confluence .
docker tag confluence austinv11/discord4j:confluence
docker push austinv11/discord4j:confluence

cd ../jira/
docker build -t jira .
docker tag jira austinv11/discord4j:jira
docker push austinv11/discord4j:jira

cd ../flask-webhook/
docker build -t webhook .
docker tag webhook austinv11/discord4j:webhook
docker push austinv11/discord4j:webhook
