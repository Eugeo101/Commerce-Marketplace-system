CREATE TABLE LOC(
    CITY VARCHAR(25) NOT NULL PRIMARY KEY,
    COUNTRY VARCHAR(25) NOT NULL
);

CREATE TABLE USER (
    EMAIL VARCHAR(25) NOT NULL PRIMARY KEY,
    FNAME VARCHAR(25) NOT NULL,
    LNAME VARCHAR(25) NOT NULL,
    PASSWORD CHAR(32) NOT NULL,
    BDATE DATE NOT NULL,
    CITY VARCHAR(25) NOT NULL,
    JOB VARCHAR(25) NOT NULL,
    CASH FLOAT,

    FOREIGN KEY (CITY) REFERENCES LOC(CITY)
);


CREATE TABLE ITEM_IDENTIFIER(
    ITEMID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    NAME VARCHAR(25) NOT NULL,
    DESCRIPTION VARCHAR(500)
);

CREATE TABLE ITEM(
    NAME VARCHAR(25) NOT NULL,
    DESCRIPTION VARCHAR(500) NOT NULL,
    IMAGE BLOB,
    PROCESSOR VARCHAR(25) NOT NULL,
    MEMORY VARCHAR(25) NOT NULL,
    STORAGE VARCHAR(25) NOT NULL,
    MANUFACT VARCHAR(25) NOT NULL,
    PRICE FLOAT NOT NULL,
    STOCK INTEGER NOT NULL,

    PRIMARY KEY(NAME, DESCRIPTION)
);

CREATE TABLE PURCHASES(
    PURCHID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    EMAIL VARCHAR(25) NOT NULL,
    ITEMID INTEGER NOT NULL,
    QUANTITY INTEGER,
    DTIME DATETIME,
    TOTALPRICE FLOAT,
    STATUS INTEGER NOT NULL,

    FOREIGN KEY (EMAIL) REFERENCES USER(EMAIL),
    FOREIGN KEY (ITEMID) REFERENCES ITEM_IDENTIFIER(ITEMID)
);