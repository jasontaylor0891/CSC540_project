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
('jmosher', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 1),
('ehope', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 3),
('eorenstein', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 3),
('jkelly', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 2),
('jillt', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('billw', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('jakew', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('katek', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('ctaylor', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4),
('kimt', '$5$rounds=535000$t6Y73jKPWxeNh9Ru$teQmHgaGdlo6U/xUzdYoK414w9P7Uhyu2b5GIA1tGv1', 4);



CREATE TABLE Branch(
    branch_No INT PRIMARY KEY AUTO_INCREMENT,
    branch_Name  VARCHAR(25) NOT NULL,
    address VARCHAR(60) NOT NULL, 
    city VARCHAR(25) NOT NULL,
    zipCode VARCHAR(5) NOT NULL,
    phoneNum VARCHAR(12) NOT NULL
);

INSERT INTO Branch(branch_Name, address, city, zipCode, phoneNum) 
VALUES 
('Power Fitness New Haven', '142 Church St', 'New Haven', '06501', '203-555-1234'),
('Power Fitness Milford', '1258 Boston Post Rd', 'Milford', '06460', '203-555-1234'),
('Power Fitness Stamford', '888 Main St', 'Stamford', '06901', '203-555-1234');

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
    branch_No INT NOT NULL,
    username VARCHAR(30) NOT NULL,
    FOREIGN KEY (username) REFERENCES logins(username),
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( 'Jill', 'Taylor', 32, 'Female', '21 Chidsey Dr', 'Northford', '06471', 1, 'Platinum', 99.95, 'jillt', 1);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( 'Bill', 'West', 28, 'Male', '883 Elm St', 'New Haven', '06501', 1, 'Platinum', 99.95, 'billw', 3);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( 'Jake', 'Wall', 45, 'Male', '182 Ridge St', 'Stanford', '06901', 1, 'Gold', 49.95, 'jakew', 1);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( 'Kate', 'Kyle', 38, 'Female', '192 Church St', 'New Haven', '06501', 1, 'Gold', 49.95, 'katek', 1);
INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( 'Kim', 'Tyler', 18, 'Female', '1209 State St', 'New Haven', '06501', 1, 'Sliver', 25.00, 'kimt', 1);

CREATE TABLE Employees(
    employee_ID INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(255),
    lastName VARCHAR(255) NOT NULL,
    branch_No INT NOT NULL,
    position VARCHAR(30),
    salary INT,
    username VARCHAR(30) NOT NULL,
    FOREIGN KEY (username) REFERENCES logins(username),
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);

INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( 'Jake', 'Mosher', 1, 'Manager', '89000', 'jmosher');
INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( 'emily', 'hope', 1, 'Trainer', '48500', 'ehope');
INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( 'Ella', 'Orenstein', 1, 'Trainer', '45000', 'eorenstein');
INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( 'John', 'Kelly', 1, 'Receptionist', '36500', 'jkelly');
INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( 'Cindy', 'Taylor', 1, 'Receptionist', '38000', 'ctaylor');

CREATE TABLE Classes(
    class_ID INT PRIMARY KEY AUTO_INCREMENT,
    instructor_ID INT,
    branch_No INT,
    class_name VARCHAR(30),
    class_type VARCHAR(30),
    class_desc VARCHAR(250),
    time_start TIME,
    date_start DATE,
    available_slots INT,
    FOREIGN KEY (instructor_ID) REFERENCES Employees(employee_ID) ON DELETE SET NULL,
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);


INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Cardio Barre - Any Level', 'Cardio', 'Barre movements with intervals of cardio. There is minimal impact but dont let that fool you. One of the best workouts with standing and seated work. Mat needed.', '08:00', '2021-12-01', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Cardio Barre - Any Level', 'Cardio', 'Barre movements with intervals of cardio. There is minimal impact but dont let that fool you. One of the best workouts with standing and seated work. Mat needed.', '08:00', '2021-12-07', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Cardio Barre - Any Level', 'Cardio', 'Barre movements with intervals of cardio. There is minimal impact but dont let that fool you. One of the best workouts with standing and seated work. Mat needed.', '08:00', '2021-12-14', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Cardio Barre - Any Level', 'Cardio', 'Barre movements with intervals of cardio. There is minimal impact but dont let that fool you. One of the best workouts with standing and seated work. Mat needed.', '08:00', '2021-12-21', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Cardio Barre - Any Level', 'Cardio', 'Barre movements with intervals of cardio. There is minimal impact but dont let that fool you. One of the best workouts with standing and seated work. Mat needed.', '08:00', '2021-12-27', 15);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'R.I.P.P.E.D. - Any Level', 'Cardio', 'An energizing workout, utilizing resistance and cardio training, which masterfully combines resistance, intervals,power, plyometrics, and endurance. All levels.', '09:00', '2021-12-02', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'R.I.P.P.E.D. - Any Level', 'Cardio', 'An energizing workout, utilizing resistance and cardio training, which masterfully combines resistance, intervals,power, plyometrics, and endurance. All levels.', '09:00', '2021-12-08', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'R.I.P.P.E.D. - Any Level', 'Cardio', 'An energizing workout, utilizing resistance and cardio training, which masterfully combines resistance, intervals,power, plyometrics, and endurance. All levels.', '09:00', '2021-12-15', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'R.I.P.P.E.D. - Any Level', 'Cardio', 'An energizing workout, utilizing resistance and cardio training, which masterfully combines resistance, intervals,power, plyometrics, and endurance. All levels.', '09:00', '2021-12-22', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'R.I.P.P.E.D. - Any Level', 'Cardio', 'An energizing workout, utilizing resistance and cardio training, which masterfully combines resistance, intervals,power, plyometrics, and endurance. All levels.', '09:00', '2021-12-28', 15);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Group Cycling - Any Level', 'Spin', 'A fun group class performed on a stationary cycling bike. This class combines a cardio and strength training workout for all levels.', '10:30', '2021-12-03', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Group Cycling - Any Level', 'Spin', 'A fun group class performed on a stationary cycling bike. This class combines a cardio and strength training workout for all levels.', '10:30', '2021-12-09', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Group Cycling - Any Level', 'Spin', 'A fun group class performed on a stationary cycling bike. This class combines a cardio and strength training workout for all levels.', '10:30', '2021-12-16', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Group Cycling - Any Level', 'Spin', 'A fun group class performed on a stationary cycling bike. This class combines a cardio and strength training workout for all levels.', '10:30', '2021-12-23', 10);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Zumba', 'Dance', 'Easy to follow class that lets you move to the beat at your own speed. Invigorating, community-oriented dance-fitness class that feels fresh and exhilarating! Modified, low-impact moves available for active older adults.', '11:00', '2021-12-01', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Zumba', 'Dance', 'Easy to follow class that lets you move to the beat at your own speed. Invigorating, community-oriented dance-fitness class that feels fresh and exhilarating! Modified, low-impact moves available for active older adults.', '11:00', '2021-12-07', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Zumba', 'Dance', 'Easy to follow class that lets you move to the beat at your own speed. Invigorating, community-oriented dance-fitness class that feels fresh and exhilarating! Modified, low-impact moves available for active older adults.', '11:00', '2021-12-14', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 2, 1, 'Zumba', 'Dance', 'Easy to follow class that lets you move to the beat at your own speed. Invigorating, community-oriented dance-fitness class that feels fresh and exhilarating! Modified, low-impact moves available for active older adults.', '11:00', '2021-12-21', 15);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Body Sculpting - Any Level', 'Strength', 'The overall muscle conditioning workout increases strength, endurance and stamina using weights, tubing, body bars, bands and exercise balls.', '13:00', '2021-12-03', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Body Sculpting - Any Level', 'Strength', 'The overall muscle conditioning workout increases strength, endurance and stamina using weights, tubing, body bars, bands and exercise balls.', '13:00', '2021-12-10', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Body Sculpting - Any Level', 'Strength', 'The overall muscle conditioning workout increases strength, endurance and stamina using weights, tubing, body bars, bands and exercise balls.', '13:00', '2021-12-17', 15);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Body Sculpting - Any Level', 'Strength', 'The overall muscle conditioning workout increases strength, endurance and stamina using weights, tubing, body bars, bands and exercise balls.', '13:00', '2021-12-25', 15);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Pilates Mat - Any Level', 'Mind & Body', 'Tone and strengthen core muscles, improve stability and posture, slim down and tone up. This class involves free flowing moves concentrating on core strength, muscle balance, flexibility by doing traditional Pilates on a mat and stability ball.', '16:00', '2021-12-04', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Pilates Mat - Any Level', 'Mind & Body', 'Tone and strengthen core muscles, improve stability and posture, slim down and tone up. This class involves free flowing moves concentrating on core strength, muscle balance, flexibility by doing traditional Pilates on a mat and stability ball.', '16:00', '2021-12-11', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Pilates Mat - Any Level', 'Mind & Body', 'Tone and strengthen core muscles, improve stability and posture, slim down and tone up. This class involves free flowing moves concentrating on core strength, muscle balance, flexibility by doing traditional Pilates on a mat and stability ball.', '16:00', '2021-12-18', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Pilates Mat - Any Level', 'Mind & Body', 'Tone and strengthen core muscles, improve stability and posture, slim down and tone up. This class involves free flowing moves concentrating on core strength, muscle balance, flexibility by doing traditional Pilates on a mat and stability ball.', '16:00', '2021-12-26', 10);

INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Boot Camp - Land - Any Level', 'Cardio', 'A high intensity workout designed to work the whole body using resistance equipment, steps and high intensity floor exercise.', '18:00', '2021-12-05', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Boot Camp - Land - Any Level', 'Cardio', 'A high intensity workout designed to work the whole body using resistance equipment, steps and high intensity floor exercise.', '18:00', '2021-12-12', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Boot Camp - Land - Any Level', 'Cardio', 'A high intensity workout designed to work the whole body using resistance equipment, steps and high intensity floor exercise.', '18:00', '2021-12-19', 10);
INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 3, 1, 'Boot Camp - Land - Any Level', 'Cardio', 'A high intensity workout designed to work the whole body using resistance equipment, steps and high intensity floor exercise.', '18:00', '2021-12-26', 10);

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
    description VARCHAR(250),
    date_Purchased DATE,
    FOREIGN KEY (branch_No) REFERENCES Branch(branch_No)
);

INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack EXP 7i Treadmill', 1, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack EXP 7i Treadmill', 2, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack EXP 7i Treadmill', 3, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');

INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack Commercial 14.9 Elliptical', 1, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack Commercial 14.9 Elliptical', 2, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack Commercial 14.9 Elliptical', 3, 'Bluetooth compatible audio with dual 2-inch speakers, Smart HD touchscreen', '2021-10-30');

INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('Bowflex M6 Max Trainer', 1, 'The Bowflex M6 Max Trainer machine offers an attractive way to get the benefits of the JRNY App at an affordable price.', '2021-10-15');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('Bowflex M6 Max Trainer', 2, 'The Bowflex M6 Max Trainer machine offers an attractive way to get the benefits of the JRNY App at an affordable price.', '2021-10-15');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('Bowflex M6 Max Trainer', 3, 'The Bowflex  M6 Max Trainer machine offers an attractive way to get the benefits of the JRNY App at an affordable price.', '2021-10-15');

INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack S22i Studio Cycle', 1, 'The NordicTrack S22i Studio Cycle is revolutionizing the home gym cycling experience.', '2021-10-15');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack S22i Studio Cycle', 2, 'The NordicTrack S22i Studio Cycle is revolutionizing the home gym cycling experience.', '2021-10-15');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack S22i Studio Cycle', 3, 'The NordicTrack S22i Studio Cycle is revolutionizing the home gym cycling experience.', '2021-10-15');

INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack RW600 Rower', 1, 'NordicTrack RW600 Rower', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack RW600 Rower', 2, 'NordicTrack RW600 Rower', '2021-10-30');
INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES('NordicTrack RW600 Rower', 3, 'NordicTrack RW600 Rower', '2021-10-30');

CREATE TABLE ClassTypes(
    class_Type VARCHAR(25) PRIMARY KEY
);

INSERT INTO ClassTypes(class_Type) 
VALUES
('Cardio'),
('Dance'),
('Mind & Body'),
('Strength'),
('Spin');

CREATE TABLE ClassTimes(
    class_Times VARCHAR(50) PRIMARY KEY
);

INSERT INTO ClassTimes(class_Times) 
VALUES
('08:00'),('08:30'),('09:00'),('09:30'),('10:00'),('10:30'),
('11:00'),('11:30'),('12:00'),('12:30'),('13:00'),('13:30'),
('14:00'),('14:30'),('15:00'),('15:30'),('16:00'),('16:30'),
('17:00'),('17:30'),('18:00'),('18:30'),('19:00'),('19:30');
