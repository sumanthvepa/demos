#!/bin/bash
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
######################################################################

echo `mysql --user=svepa --password secrets -N -s -e 'select secret_value from secret where environment_variable_name="AUTH_APP_FLASK_SECRET_KEY" and environment_name="development"'`
