drop table if exists distinct_issuers;
create table distinct_issuers(issuer_name varchar(32), search_term varchar(32), address varchar(128));
.mode csv
.import distinct_issuers.csv distinct_issuers
