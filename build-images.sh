#!/usr/bin/env bash

 
#cd ./web-frontend/
#docker build -t web-frontend .
#docker tag web-frontend austinv11/discord4j:web-frontend
#docker push austinv11/discord4j:web-frontend

# Expecting the discord4j-web repo to be cloned in the parent dir!
cd ../discord4j-web
docker build -t web-frontend .
docker tag web-frontend austinv11/discord4j:web-frontend
docker push austinv11/discord4j:web-frontend

cd ../Dockerfiles

cd ./web-old/
docker build -t web-old .
docker tag web-old austinv11/discord4j:web-old
docker push austinv11/discord4j:web-old

cd ../nginx/
docker build -t nginx .
docker tag nginx austinv11/discord4j:nginx
docker push austinv11/discord4j:nginx

cd ../database/
docker build -t database .
docker tag database austinv11/discord4j:database
docker push austinv11/discord4j:database

cd ../flask-webhook/
docker build -t webhook .
docker tag webhook austinv11/discord4j:webhook
docker push austinv11/discord4j:webhook

cd ../internal-api/
docker build -t github .
docker tag github austinv11/discord4j:github
docker push austinv11/discord4j:github

cd ..
