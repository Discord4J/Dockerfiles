#!/usr/bin/env bash

if [ "$(id -u)" != "0" ]; then # Docker compose requires root privleges
   echo "This script must be run as root" 1>&2
   exit 1
fi

ARCH="amd64"  # armhf required?

echo "Installing docker ce..."
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

add-apt-repository \
   "deb [arch=$ARCH] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update

apt-get install docker-ce

echo "Checking installation status..."
docker run hello-world

echo "Enabling systemd service..."
systemctl enable docker

echo "Installing docker compose..."
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

docker-compose --version

echo "Installing docker completions..."
curl -L https://raw.githubusercontent.com/docker/compose/1.21.2/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose

echo "Done!"
exit 0
