CREATE TABLE valid_items (
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE
);

CREATE TABLE rejected_items (
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE,
    is_valid VARCHAR,
    validation_reason VARCHAR
);

CREATE TABLE duplicate_items (
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE,
    score INTEGER
);

create table sp500_companies (
    company VARCHAR NOT NULL
);
