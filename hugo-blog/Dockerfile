FROM alpine:3.23

RUN apk upgrade --no-cache && \
    apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community hugo && \
    addgroup hugo-group && adduser -S -G -D hugo-user

WORKDIR /src


# hugp's development server uses port 1313 by default
EXPOSE 1313
    
CMD ["hugo", "server", "-D"]
