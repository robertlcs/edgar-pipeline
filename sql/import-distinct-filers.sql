drop table if exists distinct_filers;
create table distinct_filers(filing_person varchar(32),
                             issuer_name varchar(32),
                             search_term varchar(32),
                             address varchar(128));
.mode csv
.import distinct_filers.csv distinct_filers
