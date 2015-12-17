import os

from cleaning import strip_issuer_name

os.system("python extract_cusip6_from_valid_items.py")
os.system("python add_issuer_name_stem.py issuer-cusip6s.csv")
os.system("mv issuer-cusip6s-with-stems.csv issuer_cusip6_with_stems.csv")

# Query the issuer-cusip6s.csv file to get the distinct filing entities, using the search term to find similar names.
# We now use either the filing person or the issuer_name, if it's available. Note that || '%' concatenates
# the wildcard % to the query term. This is special querycsv SQL syntax.
os.system('''querycsv.py -i issuer_cusip6_with_stems.csv -o distinct_filers.csv "select distinct filing_person, issuer_name, search_term, address from issuer_cusip6_with_stems where (filing_person like stem || '%' or issuer_name like stem || '%') and address not like ''"
''')
os.system("tail -n+2 distinct_filers.csv > distinct_filers.csv.tmp; mv distinct_filers.csv.tmp distinct_filers.csv")
os.system("sqlite3 ingest.db < sql/import-distinct-filers.sql")

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
        query = "select count(*) from distinct_filers where issuer_name like '" + strip_issuer_name(company) + "%'"\
                " or filing_person like '" + strip_issuer_name(company) + "%'"
        #print query
        cur.execute(query)
        row = cur.fetchone()
        #print row
        if row[0] == 0:
            print company
            writer.writerow([company])



