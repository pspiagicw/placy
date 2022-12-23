FROM ubuntu:latest

MAINTAINER pspiagicw

WORKDIR /app

COPY . /app

WORKDIR /app/backend

RUN apt update && apt install -y python3-pip && apt install -y git && pip install poetry poethepoet && poe init

CMD ["poe","run"]
