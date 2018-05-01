PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('0687f67cd144');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(64), 
	email VARCHAR(120), 
	password_hash VARCHAR(128), about_me VARCHAR(140), last_seen DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO user VALUES(1,'susan','rlvmw@outlook.com','pbkdf2:sha256:50000$LjiCehr4$543f9fbd891bfaaa5f995d46804d132848af65083d4402a55d27780158913c9c','','2018-05-01 10:49:14.161464');
CREATE TABLE post (
	id INTEGER NOT NULL, 
	body VARCHAR(140), 
	timestamp DATETIME, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE UNIQUE INDEX ix_user_username ON user (username);
CREATE INDEX ix_post_timestamp ON post (timestamp);
COMMIT;
