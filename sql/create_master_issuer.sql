CREATE TABLE master_issuers (
	cusip_6 VARCHAR(6) NOT NULL,
    issuer_name VARCHAR(32) NOT NULL
);

create index issuer_name_ndx ON master_issuers (issuer_name);
create index cusip6_ndx ON master_issuers (cusip_6);

