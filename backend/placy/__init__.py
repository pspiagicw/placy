r"""
# The `placy` backend API.

This serves as the backend for the Placement Dashboard App.

This is the `code` documentation if you want the API documentation click [here](/redoc)

This is a `fastapi` app which has multiple services built into it.
- Authentication API.

## External Services

This also depends on some external services.
- `sendgrid` for sending transactional emails.
- `mongodb` for storing the data.

## Parts

The code is broken down into 5 parts.

- `routes` stores the API routes. This code is responsible for decoding requests and validating JSON bodies.

- `controllers` stores the code for executing the actions needed for the change requested.

- `models` stores all the models used by the application. There are 3 subtypes to it.

- `services` stores all the services needed by the application. This is done to improve testing and add Dependency Injection.

- `tests` stores all the end-to-end testing performed on the API. Due to lack of time unit testing is mostly skipped. They provide mock dependencies in most cases.

## Installation and Usage.

For running the application you have 2 choices. Either use `docker` or clone the repo and manually run it.

This webpage is through a docker image.

### Docker Installation

The application's latest docker image can be found on DockerHub with the name `pspiagicw/placy`.

It only has 1 tag `latest`. By default it runs on port `5000`.


```sh
# Port forward port 5000 in container to port 80 on host.
docker run -p 80:5000 pspiagicw/placy:latest
```

### Manual Installation

Clone the repository `https://github.com/pspiagicw/placy`.

Then change into the `backend` directory where all further instructions will be followed.

#### Prerequisites

For installing and running the code you need 2 `PyPi` packages `poetry` and `poethepoet`.

You can install this using `pip/pipx`.

If using `pip`

```sh
pip install poethepoet poetry
```

If using `pipx`

```sh
pipx install poethepoet
pipx install poetry
```

#### Installing Dependencies

Creating a virtualenv and installing dependencies is handled by `poetry`.
`poethepoet` is a task runner built upon poetry. You can use it instead of writing every command yourself.


Run
```sh
poe install
```
This would create a virtualenv, install all depdencies. Currently it installs all dependencies (development and production).

To run the application
simply used

```
poe run
```
"""
