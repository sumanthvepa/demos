
INSERT INTO `secret` (
    `secret_id`, `secret_name`, `environment_name`,
    `environment_variable_name`, `secret_value`, `description`) VALUES
  (1, "auth_app_flask_secret_key", "development",
  "AUTH_APP_FLASK_SECRET_KEY", "THE SECRET KEY GOES HERE",
  "The secret key used in the auth demo running on nines");
