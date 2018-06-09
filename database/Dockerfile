FROM postgres:10.4-alpine
WORKDIR /var/lib/postgresql/data/
# Place postgres files (/var/lib/postgresql/<version>/main) in the same directory as the docker file to add it
ADD . .
EXPOSE 5432
#TODO: add confluence and jira users