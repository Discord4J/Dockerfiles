# Forked from https://github.com/keeganwitt/docker-gradle/blob/master/jdk10-slim/Dockerfile but uses a separate volume
FROM openjdk:%JAVA_VERSION%-jdk-slim

CMD ["gradle"]

ENV GRADLE_HOME /opt/gradle/%JAVA_VERSION%
ENV GRADLE_VERSION 4.8.1

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		unzip \
		wget && \
	rm -rf /var/lib/apt/lists/*

ARG GRADLE_DOWNLOAD_SHA256=af334d994b5e69e439ab55b5d2b7d086da5ea6763d78054f49f147b06370ed71
RUN set -o errexit -o nounset \
	&& echo "Downloading Gradle" \
	&& wget --no-verbose --output-document=gradle.zip "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" \
	\
	&& echo "Checking download hash" \
	&& echo "${GRADLE_DOWNLOAD_SHA256} *gradle.zip" | sha256sum --check - \
	\
	&& echo "Installing Gradle" \
	&& unzip gradle.zip \
	&& rm gradle.zip \
	&& mv "gradle-${GRADLE_VERSION}" "${GRADLE_HOME}/" \
	&& ln --symbolic "${GRADLE_HOME}/bin/gradle" /usr/bin/gradle \
	\
	&& echo "Adding gradle user and group" \
	&& groupadd --system --gid 1000 gradle \
	&& useradd --system --gid gradle --uid 1000 --shell /bin/bash --create-home gradle \
	&& mkdir /home/gradle/.gradle \
	&& chown --recursive gradle:gradle /home/gradle \
	\
	&& echo "Symlinking root Gradle cache to gradle Gradle cache" \
	&& ln -s /home/gradle/%JAVA_VERSION%/.gradle /root/.gradle

# Create Gradle volume
USER gradle
VOLUME "/home/gradle/%JAVA_VERSION%/.gradle"
WORKDIR /home/gradle/%JAVA_VERSION%

RUN set -o errexit -o nounset \
	&& echo "Testing Gradle installation" \
	&& gradle --version