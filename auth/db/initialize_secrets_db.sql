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

CREATE TABLE `secret` (
  `secret_id` INT(11) UNSIGNED NOT NULL PRIMARY KEY,
  `secret_name` VARCHAR(64) NOT NULL,
  `environment_name` VARCHAR(32) NOT NULL,
  `environment_variable_name` VARCHAR(64) NOT NULL,
  `secret_value` VARCHAR(128) NOT NULL,
  `description` VARCHAR(256) NOT NULL,

  UNIQUE (`secret_name`),

  INDEX `en_evn_index` (`environment_name`, `environment_variable_name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

