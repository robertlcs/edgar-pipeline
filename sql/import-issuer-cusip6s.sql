drop table if exists issuer_cusip6s;
create table issuer_cusip6s(CUSIP6 varchar(32),
                            SEARCH_TERM varchar(32),
                            ISSUER_NAME varchar(32),
                            FILING_PERSON varchar(32),
                            ADDRESS varchar(128),
                            DOCUMENT_NAME varchar(32),
                            DOCUMENT_TYPE varchar(32));
.mode csv
.import issuer_cusip6s.csv issuer_cusip6s
