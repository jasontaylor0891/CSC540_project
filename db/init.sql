CREATE DATABASE gym;
use gym;

CREATE USER 'gym'@'%%' IDENTIFIED BY 'welcome123';
GRANT ALL PRIVILEGES ON * . * TO 'gym'@'%%';
FLUSH PRIVILEGES;

CREATE TABLE membershipsTypes(
    membershipsTypes_ID INT,
    membershipsTypesName VARCHAR(25),
    fee float,
    PRIMARY KEY(membershipsTypes_ID)
);

INSERT INTO membershipsTypes(membershipsTypes_ID, membershipsTypesName, fee)
VALUES
(1, 'Platinum', 99.95),
(2, 'Gold', 49.95),
(3, 'Sliver', 25.00);

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


CREATE TABLE Branch(
    branch_No INT PRIMARY KEY AUTO_INCREMENT,
    address VARCHAR(60) NOT NULL
);

CREATE TABLE Customers(
    customer_ID INT NOT NULL AUTO_INCREMENT,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(6) NOT NULL,
    Address VARCHAR(60) NOT NULL,
    city VARCHAR(25) NOT NULL,
    zipCode VARCHAR(5) NOT NULL,
    membership_ID INT NOT NULL,
    membership_type VARCHAR(10) NOT NULL,
    fee FLOAT NOT NULL,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(250) NOT NULL,
    PRIMARY KEY ( customer_ID )
);

CREATE TABLE Employees(
    employee_ID INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(255),
    lastName VARCHAR(255) NOT NULL,
    branch_No INT,
    position VARCHAR(30),
    salary INT,
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);

CREATE TABLE Classes(
    class_ID INT PRIMARY KEY AUTO_INCREMENT,
    instructor_ID INT,
    branch_No INT,
    class_type VARCHAR(30),
    time_start TIME,
    date_start DATE,
    available_slots INT,
    FOREIGN KEY (instructor_ID) REFERENCES Employees(employee_ID),
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);

CREATE TABLE MemberClasses(
    customer_ID INT NOT NULL AUTO_INCREMENT,
    class_ID INT NOT NULL,
    PRIMARY KEY(customer_ID, class_ID),
    FOREIGN KEY(customer_ID)
        REFERENCES Customers(customer_ID),
    FOREIGN KEY(class_ID)
        REFERENCES Classes(class_ID)
);

CREATE TABLE CustomerBranch(
    customer_ID INT NOT NULL AUTO_INCREMENT,
    branch_No INT NOT NULL,
    PRIMARY KEY(customer_ID, branch_No),
    FOREIGN KEY(customer_ID)
        REFERENCES Customers(customer_ID),
    FOREIGN KEY(branch_No)
        REFERENCES Branch(branch_No)
);

CREATE TABLE Equipment(
    equipment_ID INT PRIMARY KEY AUTO_INCREMENT,
    equipment_Type VARCHAR(50),
    branch_No INT,
    description VARCHAR(50),
    date_Purchased DATE,
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);