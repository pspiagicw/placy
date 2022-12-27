FROM ubuntu:latest

MAINTAINER pspiagicw

RUN apt update && apt install -y python3-pip && apt install -y git

WORKDIR /app

COPY . /app

WORKDIR /app/backend

RUN pip install poetry poethepoet && poe init-simple

CMD ["poe","run"]
