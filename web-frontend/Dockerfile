FROM node:alpine as yarn_build

WORKDIR /yarnstuff/

RUN apk update && apk upgrade && apk add --no-cache bash git openssh

RUN yarn global add @vue/cli && yarn global add dts-gen

RUN git clone https://github.com/Discord4J/discord4j-web.git

# Must be after the clone
WORKDIR discord4j-web
ADD . discord4j-web

RUN yarn install && yarn types && yarn build

# Not scratch because it will not work in docker compose
FROM tianon/true

WORKDIR /dist/
COPY --from=yarn_build /yarnstuff/discord4j-web/dist/ .