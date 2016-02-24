import os

from cleaning import strip_issuer_name

os.system("python extract_cusip6_from_valid_items.py")
os.system("tail -n+2 issuer_cusip6s.csv > issuer_cusip6s.csv.tmp; mv issuer_cusip6s.csv.tmp issuer_cusip6s.csv")
os.system("sqlite3 ingest.db < sql/import-issuer-cusip6s.sql")

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
        #"select count(*) from issuer_cusip6s where issuer_name like 'TWENTY FIRST CENTURY FOX%' or filing_person like 'TWENTY FIRST CENTURY FOX%'"
        query = "select count(*) from issuer_cusip6s where (issuer_name like '" + strip_issuer_name(company) + "%'"\
                " or filing_person like '" + strip_issuer_name(company) + "%') and address not like ''"
        cur.execute(query)
        row = cur.fetchone()

        if row[0] == 0:
            print company
            writer.writerow([company])



