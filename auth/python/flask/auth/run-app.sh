#!/bin/sh

# TODO: Source the virtual environment if it has not
# already been sourced

cd auth;
FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=auth flask run --host=0.0.0.0

