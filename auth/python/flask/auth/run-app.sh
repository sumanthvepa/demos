#!/bin/sh

# TODO: Source the virtual environment if it has not
# already been sourced

# The environment variable AUTH_APP_FLASK_SECRET_KEY should be
# set to the value appropriate for the FLASK_ENV specified below
# in order for the service to start. Use the get_secret_key script
# in the db directory to retrive the value of the secret key.
# This can be done as follows:
# export AUTH_APP_FLASK_SECRET_KEY=`get_secret_key.sh`

# TODO: check if the AUTH_APP_FLASK_SECRET_KEY variable has been
# set, if not call get_secret_key to get the secret key and
# assign it to the environment variable and export the variable

cd auth;
FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=auth flask run --host=0.0.0.0

