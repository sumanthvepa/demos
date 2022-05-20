/*
 * This file is part of demos.
 * Demos is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * Demos is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with Foobar. If not, see <https://www.gnu.org/licenses/>.
 */
/*
  authentication_scheme
  A table describing all possible authentication schemes supported by
  this application.

  The following authentication schemes should be supported:

    username_password: A username and password authentication scheme.
    Here the user provides a username and a password to signin to the
    system. Usernames are expected to be unique in the application.
   
    email_password: An email addresss and password authentication scheme.
    Here an email address is used as an identifier for the user. Email
    addresses are expected to be unique in the application.
*/
CREATE TABLE `authentication_scheme` (
  `authentication_scheme_id` INT(11) UNSIGNED NOT NULL PRIMARY KEY,
  `name` CHAR(20) NOT NULL,
  `description` VARCHAR(255) NOT NULL,

  UNIQUE(`name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `authentication_scheme` (
    `authentication_scheme_id`, `name`, `description`) VALUES
  (1, "username_password", "A username and password authentication scheme"),
  (2, "email_password", "An email and password authentication scheme"),
  (3, "oauth_linkedin", "OAuth authenication using LinkedIn"),
  (4, "oauth_facebook", "OAuth authenication using Facebook"),
  (5, "oauth_google", "OAuth authenication using Google");


CREATE TABLE `user` (
  `user_id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `display_name` VARCHAR(64) NOT NULL,

  INDEX `display_name_index` (`display_name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `user_authentication_schemes` (
  `user_id` INT(11) UNSIGNED NOT NULL,
  `authentication_scheme_id` INT(11) UNSIGNED NOT NULL,

  PRIMARY KEY(`user_id`, `authentication_scheme_id`),

  CONSTRAINT `fk_user_authentication_schemes_user`
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),

  CONSTRAINT `fk_user_authentication_schemes_authentication_scheme`
    FOREIGN KEY (`authentication_scheme_id`)
    REFERENCES authentication_scheme(`authentication_scheme_id`),

  INDEX `user_id_index` (`user_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE username (
  `user_id` INT(11) UNSIGNED NOT NULL PRIMARY KEY,
  `username` CHAR(32) NOT NULL,

  UNIQUE (`username`),

  CONSTRAINT `fk_username_user` FOREIGN KEY (`user_id`)
    REFERENCES user(`user_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE email(
  `user_id` INT(11) UNSIGNED NOT NULL PRIMARY KEY,
  `email` VARCHAR(320) NOT NULL,

  UNIQUE (`email`),

  CONSTRAINT `fk_email_user` FOREIGN KEY (`user_id`)
    REFERENCES user(`user_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE password (
  `user_id` INT(11) UNSIGNED NOT NULL PRIMARY KEY,
  `password_hash` CHAR(128) NOT NULL,

  CONSTRAINT `fk_password_user` FOREIGN KEY (`user_id`)
    REFERENCES user(`user_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


/* These tables are for demonstration purposes only */
CREATE TABLE url(
  `url_id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 `url_hash` CHAR(128) NOT NULL,
 `full_url` VARCHAR(2048) NOT NULL,

 UNIQUE(`url_hash`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE user_urls (
  `user_id` INT(11) UNSIGNED NOT NULL,
  `url_id` INT(11) UNSIGNED NOT NULL,

  PRIMARY KEY(`user_id`, `url_id`),

  CONSTRAINT `fk_user_url_user` FOREIGN KEY (`user_id`)
    REFERENCES user(`user_id`),

  CONSTRAINT `fk_user_url_url` FOREIGN KEY (`url_id`)
    REFERENCES url(`url_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Alternate design for a user table. Not chosen because it is not 3NF 
CREATE TABLE alternate_user (
  `user_id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(32) NULL,
  `email` VARCHAR(320) NULL,
  `display_name` VARCHAR(32) NOT NULL,

  `at_least_one_of` VARCHAR(320)  GENERATED ALWAYS AS (coalesce(`username`, `email`)) VIRTUAL,

  CONSTRAINT `at_least_one_of_not_null` CHECK (`at_least_one_of` IS NOT NULL),

  INDEX `display_name_index` (`display_name`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
