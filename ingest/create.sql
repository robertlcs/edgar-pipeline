CREATE TABLE items (
    cusip VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    address VARCHAR,
    issue_name VARCHAR,
    issuer_name VARCHAR,
    document_name VARCHAR,
    date DATE
);

create table sp500_companies (
    company_name VARCHAR NOT NULL
);
