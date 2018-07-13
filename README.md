# Discord4J Dockerfiles
This repository contains a set of Dockerfiles used to manage
our website backend via docker-compose. Literally every
aspect of the server is managed via this, allowing for
near instant re-deployments as well as easy local cloning.

**This is not intended for general use as built images
are published to a private docker repository**.
This is just open sourced for the hope it helps users
attempting similar configurations and to help contributors
submit patches to our server without the need of admin
credentials.

## Usage
1. Install docker and docker-compose. If you are on ubuntu,
this can be achieved by running `install.sh`
2. To rebuild and publish updated images, run `build-images.sh`.
If you just want to rebuild, simply adapt that script by 
commenting out the `docker push xx` lines.
3. To start the server, run `launch.sh`.

Additionally, you should create a `.env` file which defines
environment variables.
