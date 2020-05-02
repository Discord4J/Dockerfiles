FROM python:3.8.2-alpine

ADD . /working/
WORKDIR /working/

ENV DOCKER_STAT 'yes'
ENV ACCESS_TOKEN ''

EXPOSE 7667

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "localhost:7667", "app:app"]