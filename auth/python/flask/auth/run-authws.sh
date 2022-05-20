#!/bin/sh
#####################################################################
# This file is part of demos.
# Demos is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Demos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Foobar. If not, see <https://www.gnu.org/licenses/>.
#####################################################################

# TODO: Source the virtual environment if it has not
# already been sourced


cd authws;
FLASK_DEBUG=1 FLASK_ENV=development FLASK_APP=authws flask run --host=0.0.0.0 --port=5001

