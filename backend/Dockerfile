FROM ubuntu:latest

MAINTAINER pspiagicw

WORKDIR /app

COPY . /app

RUN apt update && apt install -y python3-pip git && pip install poetry poethepoet && poe init

CMD ["poe","run"]
