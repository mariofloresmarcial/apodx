/*
@auhtor=MarioFloresMarcial
*/

CREATE DATABASE apod_db;
USE apod_db;

CREATE TABLE IF NOT EXISTS keywords (
    keywords_id INT PRIMARY KEY,
    word1 VARCHAR(150) NOT NULL,
    word2 VARCHAR(150) NOT NULL,
    word3 VARCHAR(150) NOT NULL,
    word4 VARCHAR(150) NOT NULL
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS instrument (
    instrument_id INT PRIMARY KEY,
    instrument_name VARCHAR(250) NOT NULL
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS apod (
    apod_date DATE PRIMARY KEY,
    apod_title VARCHAR(250) NOT NULL,
    apod_copyright VARCHAR(250) NOT NULL,
    apod_hd_img VARCHAR(250) NOT NULL,
    apod_img VARCHAR(250) NOT NULL,
    apod_media_type VARCHAR (10) NOT NULL,
    apod_img_type VARCHAR(10) NOT NULL,
    apod_img_width INT NOT NULL,
    apod_img_height INT NOT NULL,
    apod_explanation VARCHAR(2500) NOT NULL,
    keywords_id INT NOT NULL,
    apod_version VARCHAR(5),
    FOREIGN KEY (keywords_id) REFERENCES keywords (keywords_id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS apod_instrument (
    apod_date DATE,
    instrument_id INT,
    PRIMARY KEY (apod_date, instrument_id),
    FOREIGN KEY (apod_date) REFERENCES apod (apod_date),
    FOREIGN KEY (instrument_id) REFERENCES instrument (instrument_id)
) ENGINE=INNODB;