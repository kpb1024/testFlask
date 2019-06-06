-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS score;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS studentCourse;


CREATE TABLE user (
  id INTEGER UNSIGNED PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  auth TINYINT(1) UNSIGNED NOT NULL,
  is_male TINYINT(1) NOT NULL
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
  tname VARCHAR(10) REFERENCES teacher (name),
  dailyScoreRatio TINYINT UNSIGNED,
);


CREATE TABLE studentCourse (
  sid INTEGER UNSIGNED NOT NULL REFERENCES student (id),
  cid INTEGER UNSIGNED NOT NULL REFERENCES course (cid),
  score TINYINT UNSIGNED,
  gpa TINYINT(1) UNSIGNED,
  dailyScore TINYINT UNSIGNED,
  finalExamScore TINYINT UNSIGNED,
  is_checked TINYINT(1) DEFAULT 0,
  PRIMARY KEY ('sid', 'cid'),
  KEY 'cid' ('cid')
);

CREATE TABLE proposal (
  pid INTEGER PRIMARY KEY AUTO_INCREMENT,
  raisedTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sid INTEGER UNSIGNED NOT NULL REFERENCES student (id),
  cid INTEGER UNSIGNED NOT NULL REFERENCES course (cid),
  reason TEXT,
  reply TEXT,
  is_checked_by_teacher TINYINT(1) DEFAULT 0,
  is_checked_by_dean TINYINT(1) DEFAULT 0
);
