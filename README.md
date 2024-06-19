# flask-jouerflux

JouerFlux is an application for managing firewalls, policies, and firewall rules.

This application uses Flask as the web framework and SQLite as the database.

## Features

- Manage firewalls (add, view, delete)
- Manage policies for each firewall (add, view, delete)
- Manage firewall rules for each policy (add, view, delete)
- API documentation via Swagger
- Dockerfile for easy run and easy deployment

## Prerequisites

- Python 3.x
- Flask
- SQLite
- Docker (for deployment via container)

## Installation

1. Clone the repository:

    ```sh
    $ git clone git@github.com:0x726974636879/flask-jouerflux.git
    $ cd flask-jouerflux
    ```

2. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    $ pip install -r requirements.txt
    ```

## Run the application

1. Initialize the database:

    ```sh
    $ export FLASK_APP=$(PWD)/run.py
    $ export PYTHONPATH=$(PWD)/app

    $ flask shell
    ```

    ```python3
    >>> from app import db
    >>> db.create_all()
    ```

2. Run the application:

    ```sh
    $ flask run --host=0.0.0.0 -p 80 --reload
    ```

3. (BONUS) Run the application with docker

    ```sh
    $ docker build . --tag flask-jouerflux:latest
    $ docker run -it -p 80:5000 flask-jouerflux
    ```

## API Usage

The application exposes a RESTful API to manage firewalls, policies and firewall rules.
You can test the API via Swagger at `http://localhost/apidocs/#/`.

Access the application at `http://localhost/`.

### Endpoints

#### Firewalls

- `GET /firewalls`          : Retrieve the list of firewalls.
- `GET /firewalls/<id>`     : Retrieve a specific firewall.
- `POST /firewalls`         : Add a new firewall.
- `DELETE /firewalls/<id>`  : Delete a specific firewall.

#### Policies

- `GET /policies`           : Retrieve the list of policies.
- `POST /policies`          : Add a new policy to a firewall.
- `DELETE /policies/<id>`   : Delete a specific policy.

#### Rules

- `GET /rules`          : Retrieve the list of rules.
- `POST /rules`         : Add a new rules to a policy.
- `DELETE /rules/<id>`  : Delete a specific rule.
