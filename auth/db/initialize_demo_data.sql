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

SET autocommit  = 0;
-- Create user Lawrence Unser
START TRANSACTION;
INSERT INTO `user` (display_name) VALUES ('Lawrence Unser');
SET @user_id = LAST_INSERT_ID();
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 1);
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 2);
INSERT INTO `username` (user_id, username) VALUES (@user_id, 'luser');
INSERT INTO `email` (user_id, email) VALUES (@user_id, 'luser@example.com');
-- Password hash for '12345'
SET @password_hash = '$2b$12$l61kRf7vxg3Wm7orgem0p.t4FWu1mlwSoidFzF5y6d42/TRtXJ9/S';
INSERT INTO `password` (user_id, password_hash) VALUES (@user_id, @password_hash);
COMMIT;

-- Create user Emil O. Enly.
START TRANSACTION;
INSERT INTO `user` (display_name) VALUES ('Emile O. Enly');
SET @user_id = LAST_INSERT_ID();
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 2);
INSERT INTO `email` (user_id, email) VALUES (@user_id, 'emailonly@example.com');
-- Password hash for '12345'
SET @password_hash = '$2b$12$V0Jf7kqcoOpsnJIYxElW5eCMDNHqWRJjr1R.e9dEvRIjbyCyiBdbq';
INSERT INTO `password` (user_id, password_hash) VALUES (@user_id, @password_hash);
COMMIT;

-- Create user Uriah S. Ername.
START TRANSACTION;
INSERT INTO `user` (display_name) VALUES ('Uriah S. Ername');
SET @user_id = LAST_INSERT_ID();
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 1);
INSERT INTO `username` (user_id, username) VALUES (@user_id, 'uriah');
-- Password hash for abcde
SET @password_hash = '$2b$12$AGSEj5iqiMz99dDr7aQUNOGWmOnmVl7.Vc2E5t25KM5t/HXB/0zYG';
INSERT INTO `password` (user_id, password_hash) VALUES (@user_id, @password_hash);
COMMIT;

-- Create user Maximillian  Verstappen
START TRANSACTION;
INSERT INTO `user` (display_name) VALUES ('Max Emillian Verstappen');
SET @user_id = LAST_INSERT_ID();
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 1);
INSERT INTO `username` (user_id, username) VALUES (@user_id, 'mverstappen');
INSERT INTO `email` (user_id, email) VALUES (@user_id, 'mverstappen@example.com');
-- Password hash for password qaz4321
SET @password_hash = '$2b$12$kiwyu2UczgDSrSE9N/movO1NEBzpHGnDaXW.52ByhJl6loFgYm5yC';
INSERT INTO `password` (user_id, password_hash) VALUES (@user_id, @password_hash);
COMMIT;

-- Create user William Rowan Hamilton
START TRANSACTION;
INSERT INTO `user` (display_name) VALUES ('William Rowan Hamilton');
SET @user_id = LAST_INSERT_ID();
INSERT INTO `user_authentication_schemes` (user_id, authentication_scheme_id) VALUES  (@user_id, 1);
INSERT INTO `username` (user_id, username) VALUES (@user_id, 'william');
-- Password has for password 'aaaaaa'
SET @password_hash = '$2b$12$XwtePCJNHwPidDR3iK.InubtW3mzNWnJmZ3Hget7xFXhJiMilmcP6';
INSERT INTO `password` (user_id, password_hash) VALUES (@user_id, @password_hash);
COMMIT;
