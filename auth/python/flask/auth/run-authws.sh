#!/bin/sh
#####################################################################
# This file is part of demos project.
# (https://github.com/sumanthvepa/demos)
#
# Copyright (c) 2022 Sumanth Vepa.

# Demos is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Demos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <https://www.gnu.org/licenses/>.
#####################################################################



# TODO: Source the virtual environment if it has not already been sourced
# The following environment variables need to be set in order for the service
# to start:
# AUTHWS_FLASK_SECRET_KEY: this should be set to the value set to the value
#   appropriate for the FLASK_ENV specified below, Use the get_secret_key script
#   in the db directory to retrieve the value of the secret key. This can be
#   done as follows:
#     export AUTH_APP_FLASK_SECRET_KEY=`get_secret_key.sh`
# AUTHWS_DB_HOST: This should be set to localhost in dev and production.
#   For personal setups, it can be set to whatever machine the developer
#   desires.
# AUTHWS_DB_NAME: This should be set to liricare in dev, and production. It
#   can be set to whatever name the developer wishes for personal environments.
# AUTHWS_DB_USER: This should be set to liricare-dev in dev and liricare-prod in
#   production. It can be set to whatever the developer wishes for personal
#   environments.
# AUTHWS_DB_PASSWORD: This should be the password for liricare-dev in dev
#   and the password for liricare prod in production. It should be the password
#   for the user above in personal environments.

# TODO: check if the AUTH_APP_FLASK_SECRET_KEY variable has been
# set, if not call get_secret_key to get the secret key and
# assign it to the environment variable and export the variable


cd authws;
FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=authws flask run --host=0.0.0.0 --port=5001

