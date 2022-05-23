/********************************************************************
* This file is part of demos project.
* (https://github.com/sumanthvepa/demos)
*
* Copyright (c) 2022 Sumanth Vepa.
*
* Demos is free software: you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Demos is distributed in the hope that it will be useful, but
* WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
*  GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Foobar. If not, see <https://www.gnu.org/licenses/>.
********************************************************************/

INSERT INTO `secret` (
    `secret_id`, `secret_name`, `environment_name`,
    `environment_variable_name`, `secret_value`, `description`) VALUES
  (1, "auth_app_flask_secret_key", "development",
  "AUTH_APP_FLASK_SECRET_KEY", "THE SECRET KEY GOES HERE",
  "The secret key used in the auth demo running on nines");
