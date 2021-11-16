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
    profile INT, 
    PRIMARY KEY(username));

INSERT INTO logins(username, password, profile) 
VALUES
('admin', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 1),
('t1', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 3),
('r1', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 2),
('jillt', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('billw', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4);



CREATE TABLE Branch(
    branch_No INT PRIMARY KEY AUTO_INCREMENT,
    branch_Name  VARCHAR(25) NOT NULL,
    address VARCHAR(60) NOT NULL, 
    city VARCHAR(25) NOT NULL,
    zipCode VARCHAR(5) NOT NULL
);

INSERT INTO Branch(branch_Name, address, city, zipCode) 
VALUES 
('Power Fitness New Haven', '142 Church St', 'New Haven', '06501'),
('Power Fitness Milford', '1258 Boston Post Rd', 'Milford', '06460'),
('Power Fitness Stamford', '142 Church St', 'New Haven', '06901');

CREATE TABLE Customers(
    customer_ID INT PRIMARY KEY AUTO_INCREMENT,
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
    FOREIGN KEY (username) REFERENCES logins(username)
);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, password) VALUES( 'Jill', 'Taylor', 32, 'Female', '21 Chidsey Dr', 'Northford', '06471', 1, 'Platinum', 99.95, 'jillt', 'welcome123');
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, password) VALUES( 'Bill', 'West', 28, 'Male', '883 Elm St', 'New Haven', '06501', 1, 'Platinum', 99.95, 'billw', 'welcome123');

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