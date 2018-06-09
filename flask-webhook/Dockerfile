FROM python:3.6.5-alpine

ADD . /working/
WORKDIR /working/

ENV DOCKER_STAT 'yes'

EXPOSE 2314

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "localhost:2314", "webhook:app"]