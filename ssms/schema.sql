-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS Teach;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Deans;
DROP TABLE IF EXISTS Systemmanagers;
DROP TABLE IF EXISTS Performances;


CREATE TABLE Students (
  studentNo char(10) PRIMARY KEY;
  studentName varchar(10) NOT NULL;
  gender char(10) NOT NULL;
  studentSchool varchar(30) NOT NULL;
  major int NOT NULL;
  class varchar(30) NOT NULL;
  studentID double NOT NULL;
  studentPassword double NOT NULL;
  systemManagerNo char(10) NOT NULL;
);

CREATE TABLE Teachers (
  teacherNo char(10) PRIMARY KEY;
  teacherName varchar(30) NOT NULL;
  teacherSchool varchar(30) NOT NULL;
  teacherID double NOT NULL;
  teacherPassword double NOT NULL;
  systemManagerNo char(10) NOT NULL;
);

CREATE TABLE Deans (
  ateacherNo char(10) PRIMARY KEY;
  ateacherName varchar(30) NOT NULL;
  ateacherSchool varchar(30) NOT NULL;
  ateacherID double NOT NULL;
  ateacherPassword double NOT NULL;
  ateacherPermission varchar(255) NOT NULL;
  systemManagerNo char(10) NOT NULL;
);

CREATE TABLE Systemmanagers (
  systemManagerNo char(10) PRIMARY KEY;
  systemManagerName varchar(30) NOT NULL;
  systemManagerID double NOT NULL;
  systemManagerPassword double NOT NULL;
);


CREATE TABLE Courses (
  courseNo char(10) PRIMARY KEY;
  courseName varchar(30) NOT NULL;
  courseTerm varchar(30) NOT NULL;
  courseCate varchar(30) NOT NULL;
  creditHour double NOT NULL;
  courseHour double NOT NULL;
  teacherNo char(10) NOT NULL;
);

CREATE TABLE Performances (
  num char(10) PRIMARY KEY;
  score double NOT NULL;
  GPA double NOT NULL;
  render double NOT NULL;
  entryStatus varchar(30) NOT NULL;
  complaintStatus varchar(30) NOT NULL;
  teacherNo char(10) NOT NULL;
  studentNo char(10) FOREIGN KEY REFERENCES Students(studentNo);
  courseNo char(10) FOREIGN KEY REFERENCES Courses(courseNo);
  ateacherNo char(10) FOREIGN KEY REFERENCES Deans(ateacherNo);
);

CREATE TABLE Teach (
  studentNo char(10) PRIMARY KEY;
  teacherNo char(10) PRIMARY KEY;
  courseNo char(10) PRIMARY KEY;
);

