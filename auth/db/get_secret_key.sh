#!/bin/bash

echo `mysql --user=svepa --password secrets -N -s -e 'select secret_value from secret where environment_variable_name="AUTH_APP_FLASK_SECRET_KEY" and environment_name="development"'`
