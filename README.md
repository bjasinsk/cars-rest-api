# cars-rest-api

# Repository intended for the project which is a simple REST API - a basic database of car makes and models working with an external API.

# 1. Launching the project

# Creation of an environment

python -m venv venv

# Running the environment on a Unix-type system

source venv/bin/activate

# Running the environment on Windows

venv\Scripts\activate

# Installing the required libraries

pip install -r requirements.txt

python3.10

# To start the project using gunicorn:

gunicorn app:app
