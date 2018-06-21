FROM ruby:alpine as jekyll_build

WORKDIR /jekyllstuff/

RUN apk update && apk upgrade && apk add --no-cache bash git openssh build-base g++ make

RUN gem install jekyll bundler

RUN git clone https://github.com/Discord4J/hcz-jekyll-blog.git

# Must be after the clone
WORKDIR hcz-jekyll-blog
ADD . hcz-jekyll-blog

RUN bundle install

RUN rm -rf ./_site

RUN bundle exec jekyll build --destination ./_site

# Not scratch because it will not work in docker compose
FROM tianon/true

WORKDIR /dist/
COPY --from=jekyll_build /jekyllstuff/hcz-jekyll-blog/_site/ .