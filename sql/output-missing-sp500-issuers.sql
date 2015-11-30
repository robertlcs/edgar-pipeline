.mode csv
.output missing-sp500-issuers.csv
select * from sp500_companies where company not in (select trim(issuer_name) from distinct_issuers);

