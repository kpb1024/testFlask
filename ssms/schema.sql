-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS score;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS studentCourse;


CREATE TABLE user (
  id INTEGER UNSIGNED PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  auth TINYINT(1) UNSIGNED NOT NULL,
  is_male BIT(1) NOT NULL
);

CREATE TABLE student (
  id INTEGER UNSIGNED PRIMARY KEY REFERENCES user (id),
  name VARCHAR(10) NOT NULL
);

CREATE TABLE teacher (
  id INTEGER UNSIGNED PRIMARY KEY REFERENCES user (id),
  name VARCHAR(10) NOT NULL
);

CREATE TABLE course (
  cid INTEGER PRIMARY KEY AUTO_INCREMENT,
  cname VARCHAR(20) NOT NULL,
  courseterm TINYINT(1) UNSIGNED NOT NULL,
  courseyear YEAR NOT NULL,
  coursepoint TINYINT(1) UNSIGNED NOT NULL,
  coursetype VARCHAR(4) NOT NULL,
  tname VARCHAR(10) REFERENCES teacher (name)
);


CREATE TABLE studentCourse (
  scid INTEGER PRIMARY KEY AUTO_INCREMENT,
  sid INTEGER UNSIGNED NOT NULL REFERENCES student (id),
  cid INTEGER UNSIGNED NOT NULL REFERENCES course (cid),
  score TINYINT UNSIGNED,
  gpa TINYINT(1) UNSIGNED,
  dailyScore TINYINT UNSIGNED,
  dailyScoreRatio TINYINT UNSIGNED,
  finalExamScore TINYINT UNSIGNED,
  KEY `student` (`sid`),
  KEY `course` (`cid`)
);
