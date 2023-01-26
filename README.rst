=================
Providers Manager
=================
Providers Manager is an applition that allows users handling providers and their bank accounts for information
purposes

# Overview

This app offers a solution to create banks and attache them to providers, also allows users check the total
of records stored in a dashboard, each entity has a CRUD model used to present and handle the data in a better way.

# Technology

This project uses `FastAPI`_ framework used to speed up the development of REST API services, also it uses native
libraries and modules from python 3.9 and shared dependencies from `PyPy`_ repositories,

# Entities

The project exposes the following endpoints in general:

_user_:
These endpoints allows users register into the system and handle a login functionality with stored sessions and
permissions validation.

_providers_:
This model handles all information and functions related to providers, as their accounts and bank information.

_account_:
This model handles the account information by provider created in the system.

_bank_:
This model is used to store a basic information that will be used for the providers registration in the system.

# Creating the environment

This project could be running into a new development environment using PyEnv, this avoid a mix with other python versions or dependencies
that project will never use.

The installation depends on the OS, so you need to check the `PyEnv`\_ documentation to make the installation.

Once we have `Pyenv` installed we are ready to create our environment with the prefered python version and env name.

.. code-block:: console

    $ pyenv virtualenv 3.9.0 providers

Now that the environment is created we can initalizate it and start to work with the project.

.. code-block:: console

    $ pyenv activate providers

# Configuring the App

We can create a local service of the app, but initially we need to setup and run our MySQL database
and install all dependencies related to the project.

## Database Init

As MySQL depends on the OS, you need to check how to install in your local machine or can use a Docker
image in order to start the database service.

.. code-block:: console

    # Start mysql on macos once installed
    $ mysql.server start

## Environment Vars

Once database service is started, next step is create the application env variables, in order to do that, we need
to create a `.env` file in the root path from project, those vars will be used for app settings and connections.

.. code-block:: code

    PORT=3000
    LANGUAGE=en
    DB_HOST= "127.0.0.1" # DB_HOST=db (if connecting to a docker service)
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD="adminpass"
    DB_DATABASE="storedb"

# Installation

The application uses some public dependencies in order to run with no issues, so install is straightforward
after cloning the repository:

.. code-block:: console

    # Installing dependencies via pip
    $ pip install -r requirements.txt

# Running the App locally

Once all dependencies are solved and isnstaller we can use the next command in order to start a local server:

.. code-block:: console

    $ uvicorn app:app --reload

In order to check if app is running locally, we can open a browser and check the documentation url (`http://127.0.0.1:8000/docs`).

# Running with Doocker

This project can be executed into a docker service, in order to run it that way, we can use the `docker-compose/yml` config,
this file has already configured the database service and the application service.

Notes: Don't forget to update the `.env` file variables related to database connection

.. code-block:: code
    ...
    DB_HOST=db
    ...

Running the services:

.. code-block:: console

    $ docker-compose up provider_manager

In order to check if app is running in a docker service, we can open a browser and check the documentation url (`http://localhost/api/v1/docs`)

## Reporting bugs

If you find a bug please report it via GitHub and assign it to one of the
project owners below. If you can, please write a unittest that validates the bug and
do a PR, this make things faster :-)

# Who currently supports this project ?

- Jhon Tovar <jmtovarf@gmail.com>

.. \_PyPy: https://pypi.org/
.. \_FastAPI: https://fastapi.tiangolo.com/
.. \_PyEnv: https://github.com/pyenv/pyenv/blob/master/README.md
