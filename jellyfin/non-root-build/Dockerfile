FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir Movies Music Books && \
    curl -s https://repo.jellyfin.org/install-debuntu.sh | bash

EXPOSE 8096
