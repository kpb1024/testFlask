-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS score;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS teacher;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS studentCourse;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  auth INTEGER NOT NULL
);

CREATE TABLE student (
  sid INTEGER PRIMARY KEY,
  sname TEXT NOT NULL,
  uid INTEGER NOT NULL,
  FOREIGN KEY (uid) REFERENCES user (id)
);

CREATE TABLE teacher (
  tid INTEGER PRIMARY KEY AUTOINCREMENT,
  tname TEXT NOT NULL,
  uid INTEGER NOT NULL,
  FOREIGN KEY (uid) REFERENCES user (id)
);

CREATE TABLE course (
  cid INTEGER PRIMARY KEY AUTOINCREMENT,
  cname TEXT NOT NULL,
  courseterm INTEGER NOT NULL,
  courseyear INTEGER NOT NULL,
  coursepoint INTEGER NOT NULL,
  coursetype TEXT NOT NULL,
  tid INTEGER,
  tname TEXT,
  FOREIGN KEY (tid) REFERENCES teacher (tid),
  FOREIGN KEY (tname) REFERENCES teacher (tname)
);


CREATE TABLE studentCourse (
  sid INTEGER NOT NULL,
  cid INTEGER NOT NULL,
  scid INTEGER PRIMARY KEY AUTOINCREMENT,
  score INTEGER NOT NULL,
  gpa INTEGER NOT NULL,
  FOREIGN KEY (sid) REFERENCES student (sid),
  FOREIGN KEY (cid) REFERENCES course (cid)
);
