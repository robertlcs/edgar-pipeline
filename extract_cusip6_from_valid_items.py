import csv
import sqlite3 as lite

from company_queries import find_address
from issuer_queries import get_issuers
from valid_items_queries import find_valid_items_for_issuer

# For each company, find an address and write out each company, issuer's cusip6 and address

ID_COLUMN = 1

con = lite.connect("ingest.db")
with con:
    issuers = get_issuers(con)
    with open("issuer-cusip6s.csv", "w") as issuer_out:
        writer = csv.DictWriter(issuer_out, ['CUSIP6', 'SEARCH_TERM', 'ISSUER_NAME', 'ADDRESS'])
        writer.writeheader()
        for issuer in issuers:
            address = find_address(con, issuer[2])
            row = {}
            row['CUSIP6'] = issuer[0]
            row['SEARCH_TERM'] = issuer[1]
            row['ISSUER_NAME'] = issuer[2]
            row['ADDRESS'] = address
            writer.writerow(row)
