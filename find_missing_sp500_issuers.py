import os

os.system("python extract_cusip6_from_valid_items.py")
os.system('''querycsv.py -i issuer_cusip6 -o distinct_issuers.csv "select distinct issuer_name, search_term, address from issuer_cusip6 where issuer_name like search_term || '%' and address not like ''"
''')
os.system("tail -n+2 distinct_issuers.csv > distinct_issuers.csv.tmp; mv distinct_issuers.csv.tmp distinct_issuers.csv")
os.system("sqlite3 ingest.db < sql/import-distinct-issuers.sql")
# Import into db
# create table distinct_issuers(issuer_name varchar(32), search_term varchar(32), address varchar(128));
# .import distinct_issuers.csv distinct_issuers

#.mode csv
#.output missing-sp500-issuers
#select * from sp500_companies where company not in (select trim(issuer_name) from distinct_issuers);
os.system("sqlite3 ingest.db < sql/output-missing-sp500-issuers.sql")

