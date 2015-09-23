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

CREATE TABLE amt_batch_items (
    cusip TEXT NOT NULL,
    url TEXT NOT NULL,
    document_name TEXT NOT NULL,
    issuer_name TEXT,
    issue_name TEXT,
    address TEXT
);

create table sp500_companies (
    company VARCHAR NOT NULL
);
