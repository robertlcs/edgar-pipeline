DROP TABLE IF EXISTS valid_items;
CREATE TABLE valid_items (
    id INTEGER PRIMARY KEY ASC,
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE,
    score NUMERIC NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS rejected_items;
CREATE TABLE rejected_items (
    id INTEGER PRIMARY KEY ASC,
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE,
    validation_reason VARCHAR
);

DROP TABLE IF EXISTS duplicate_items;
CREATE TABLE duplicate_items (
    id INTEGER PRIMARY KEY ASC,
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE,
    score NUMERIC NOT NULL DEFAULT 0
);

DROP TABLE IF EXISTS amt_batch_items;
CREATE TABLE amt_batch_items (
    cusip TEXT NOT NULL,
    url TEXT NOT NULL,
    document_name TEXT NOT NULL,
    issuer_name TEXT,
    issue_name TEXT,
    address TEXT
);

DROP TABLE IF EXISTS sp500_companies;
create table sp500_companies (
    company VARCHAR NOT NULL
);
