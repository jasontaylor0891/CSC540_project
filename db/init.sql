CREATE DATABASE gym;
use gym;

CREATE USER 'gym'@'localhost' IDENTIFIED BY 'welcome123' PASSWORD EXPIRE NEVER;
GRANT ALL PRIVILEGES ON gym.* TO 'gym'@'localhost';