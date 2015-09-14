create table missing as select * from sp500_companies where company_name not in (select distinct issuer_name from items);

.mode csv
.output missing.csv
select * from missing;
.output stdout

