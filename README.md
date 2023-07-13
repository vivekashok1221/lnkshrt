# lnkshrt

lnkshrt is a URL shortener API built with FastAPI. It allows you to generate shortened URLs which redirect you to the original URLs.

The official instance of lnkshrt is hosted at [l.vivekashok.me](https://l.vivekashok.me). However, if you prefer, you can also run your own instance by following the steps in the ["Getting Started"](#getting-started) section.

The lnkshrt API is built using FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- Shorten long URLs to compact and easy-to-share shortened URLs.
- Customizable URLs with the option to specify a custom path for the shortened URL.
- Token-based authentication for secure API access.
- Delete shortened URLs when they are no longer needed.


> `lnkshrt-cli` is a command-line app with which you can easily generate shortened URLs, authenticate with your account, delete links, and perform other actions from the command-line. For detailed usage instructions and installation guide, please refer to the [lnkshrt-cli repository](https://github.com/vivekashok1221/lnkshrt-cli).


## Getting Started
To run the lnkshrt API yourself:-

1. Clone the repository:
   ```shell
   git clone https://github.com/vivekashok1221/lnkshrt.git
   ```

2. Navigate to the project directory:
   ```shell
   cd lnkshrt
   ```

3. Assuming you have Docker and Docker Compose installed on your system, you can simply run:
   ```shell
   docker compose up
   ```
   Once the containers are up and running, you can access the lnkshrt API at http://0.0.0.0:8000.


## API Documentation

You can access the API documentation online at [l.vivekashok.me](https://l.vivekashok.me) (or locally at http://0.0.0.0:8000/docs provided the server is running).


## Development

To set up the development environment for the lnkshrt API, follow the steps outlined in the ["Getting Started"](#getting-started) section above.

- ### Set up poetry env

   Assuming you have [poetry installed](https://python-poetry.org/docs/#installation), install the dependencies by running:
   ```shell
   poetry install
   ```

   To activate the poetry venv:
   ```shell
   poetry shell
   ```

- ### Set Up Pre-commit Hooks
   ```shell
   poetry run task precommit
   ```
   `pre-commit`  helps ensure code quality and consistency by automatically running various checks and formatting tools on your code before each commit.

- ### Linting

   To manually run the linting checks:
   ```shell
   poetry run task lint
   ```

- ### Generate Database Migrations
   ```shell
   poetry run alembic revision --autogenerate -m "<MESSAGE>"
   ```

## License

lnkshrt is released under the MIT License.
