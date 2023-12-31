
# SmartHouse Python Project

Welcome to the SmartHouse project! This Python application allows you to control and manage various electronic devices in your home. With the help of SQLAlchemy, Typer, and a convenient CLI, you can easily interact with your smart devices.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running in Docker](#running-in-docker)
- [Commands](#commands)
- [Modules and Libraries](#modules-and-libraries)
- [Code Quality and Linting](#code-quality-and-linting)

## Features

- Manage electronic devices such as TVs, microwaves, and air conditioners.
- Check device status and control settings.
- CLI interface for seamless interaction.
- Powered by SQLAlchemy and Typer for a robust and user-friendly experience.

## Installation

To get started with the SmartHouse project, follow these installation steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/smart-house.git
   ```

2. Change to the project directory:

   ```bash
   cd smart-house
   ```
## Usage

### Running in Docker

You can also run the SmartHouse CLI from a Docker container. To do this, make sure you have Docker and Docker Compose installed.

1. Build the Docker container:

   ```bash
   docker-compose build
   ```

2. Run the CLI from the Docker container:

   ```bash
   docker-compose run cli
   ```

This will start the CLI inside the Docker container, allowing you to interact with your smart devices.

## Commands

Here are some example commands you can use with the SmartHouse CLI:

- `python -m app.cli` - List all the available devices.
- `python -m app.cli "~device_name~"` - List all the available commands for the desired device.
- `python -m app.cli "Microwave" ON` - Set the status of a device named "Microwave" to ON.

Feel free to explore more commands by running `python -m app.cli --help`.

## Modules and Libraries

**Important built-in modules**

* *typing* module - for type hints support, specialized strongly typed classes and using advanced typing features
* *abc* module - implementing Abstract Classes
* *asyncio* module - support for async IO, futures, coroutines and tasks

**Important Python libraries**

* [*typer*](https://typer.tiangolo.com/) - create CLI applications with type hints support
* [*pydantic*](https://pydantic-docs.helpmanual.io/) - represent system entities as typed data models using type hints with many features that improve upon the built-in *dataclasses* module. Can also read application settings into data models from environment variables, secret files, and any other custom settings source, e.g. JSON files.
* [*sqlalchemy*](https://docs.sqlalchemy.org/en/20/) - Python SQL toolkit and Object Relational Mapper
* [*alembic*](https://alembic.sqlalchemy.org/en/latest/) - used as lightweight database migration tool for usage with the SQLAlchemy


## Code Quality and Linting

The following code quality and linting solutions are used:

* [*MyPy*](https://mypy.readthedocs.io/en/stable/introduction.html) - type hints checker. *pydantic* integrates with it to type check data models.
* [*black*](https://github.com/psf/black) - code formatter.
* [*isort*](https://github.com/PyCQA/isort) - sorting import statements.
* [*flake8*](https://flake8.pycqa.org/en/latest/) - Style guide enforcement. Here are some useful plugins:
  * [*flake8-builtins*](https://github.com/gforcada/flake8-builtins) - checks for accidental use of builtin functions as names
  * [*flake8-comprehensions*](https://github.com/adamchainz/flake8-comprehensions) - checks for misuse or lack of use of comprehensions
  * [*flake8-mutable*](https://github.com/ebeweber/flake8-mutable) - checks for mutable default parameter values Python issue
  * [*pep8-naming*](https://github.com/PyCQA/pep8-naming) - checks that names follow Python standards defined in PEP8
  * [*flake8-simplify*](https://github.com/MartinThoma/flake8-simplify) - checks for general Python best practices for simpler code
  * [*flake8-pytest-style*](https://github.com/m-burst/flake8-pytest-style) - check that *pytest* unit tests are written according to style; **this plugin isn't relevant for this repo**
  * [*flake8-logging-format*](https://github.com/globality-corp/flake8-logging-format) - ensures logs use extra arguments and exception(); **this plugin isn't relevant for this repo**

Note *MyPy* and *flake8* are configured with [setup.cfg](setup.cfg).
