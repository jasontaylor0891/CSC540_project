CREATE DATABASE gym;
use gym;

CREATE USER 'gym'@'%%' IDENTIFIED BY 'welcome123';
GRANT ALL PRIVILEGES ON * . * TO 'gym'@'%%';
FLUSH PRIVILEGES;

CREATE TABLE membershipsTypes(name VARCHAR(100), PRIMARY KEY(name));

INSERT INTO membershipsTypes(name)
VALUES('Gold'), ('Sliver');

CREATE TABLE logins(
    username VARCHAR(200), 
    password VARCHAR(500), 
    name VARCHAR(100), 
    profile INT, 
    PRIMARY KEY(username));

INSERT INTO logins(username, password, name, profile) 
VALUES
('admin', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 'Joe Blow', 1),
('t1', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 'Meg Gray', 3),
('r1', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 'Mat Armstrong', 2),
('m1', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 'Jill Dow', 4),
('m2', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 'Kate Hope', 4);
