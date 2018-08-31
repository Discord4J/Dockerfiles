FROM node:10-alpine as yarn_build

# Installs latest Chromium (68) package.
RUN apk update && apk upgrade && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
    apk add --no-cache \
      chromium@edge \
      nss@edge \
      bash

# Tell Puppeteer to skip installing Chrome. We'll be using the installed package.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

# Add user so we don't need --no-sandbox.
RUN addgroup -S pptruser && adduser -S -g pptruser pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && chown -R pptruser:pptruser /home/pptruser

RUN apk update && apk upgrade && apk add --no-cache bash git openssh

RUN yarn global add @vue/cli && yarn global add dts-gen

WORKDIR /yarnstuff/

RUN git clone https://github.com/Discord4J/discord4j-web.git

# Must be after the clone
WORKDIR discord4j-web
ADD . discord4j-web

RUN yarn --silent install && yarn --silent add puppeteer

RUN chown -R pptruser:pptruser /discord4j-web

USER pptruser

RUN yarn clean && yarn build 

# Not scratch because it will not work in docker compose
FROM tianon/true

WORKDIR /dist/
COPY --from=yarn_build /yarnstuff/discord4j-web/dist/ .
