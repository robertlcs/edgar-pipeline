import os

from cleaning import strip_issuer_name

os.system("python extract_cusip6_from_valid_items.py")
os.system("mv issuer-cusip6s.csv issuer_cusip6.csv")
os.system('''querycsv.py -i issuer_cusip6.csv -o distinct_issuers.csv "select distinct issuer_name, search_term, address from issuer_cusip6 where issuer_name like search_term || '%' and address not like ''"
''')
os.system("tail -n+2 distinct_issuers.csv > distinct_issuers.csv.tmp; mv distinct_issuers.csv.tmp distinct_issuers.csv")
os.system("sqlite3 ingest.db < sql/import-distinct-issuers.sql")

# Need to implement a fuzzy match to find the companies that do not have a similar issuer in distinct_issuers
import sqlite3
con = sqlite3.connect("ingest.db")
cur = con.cursor()
companies = [row[0] for row in cur.execute("select company from sp500_companies")]

import csv
with open("missing-sp500-issuers.csv", "w") as out_csv:
    writer = csv.writer(out_csv)

    for company in companies:
        #print strip_issuer_name(company)
        query = "select count(*) from distinct_issuers where issuer_name like '" + strip_issuer_name(company) + "%'"
        #print query
        cur.execute(query)
        row = cur.fetchone()
        #print row
        if row[0] == 0:
            print company
            writer.writerow([company])



