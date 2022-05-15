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

