
# SmartHouse Python Project

Welcome to the SmartHouse project! This Python application allows you to control and manage various electronic devices in your home. With the help of SQLAlchemy, Typer, and a convenient CLI, you can easily interact with your smart devices.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Running in Docker](#running-in-docker)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

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

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

5. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
6. Run the seed database script for creating devices instances:

   ```bash
   python -r requirements.txt
   ```

## Usage

### Running Locally

To run the SmartHouse CLI locally, follow these steps:

1. Make sure you're in the project directory with your virtual environment activated.


3. Run the CLI using Typer:

   ```bash
   python -m app.cli
   ```

This will start the CLI, and you can begin managing your smart devices.

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
