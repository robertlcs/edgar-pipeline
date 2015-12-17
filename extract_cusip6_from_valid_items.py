import csv
import sqlite3 as lite

from company_queries import find_address
from issuer_queries import IssuerQueries
from valid_items_queries import find_valid_items_for_issuer

# For each company, find an address and write out each company, issuer's cusip6 and address

ID_COLUMN = 1

con = lite.connect("ingest.db")
with con:
    issuers = IssuerQueries.get_issuers(con)
    with open("issuer-cusip6s.csv", "w") as issuer_out:
        writer = csv.DictWriter(issuer_out, ['CUSIP6', 'SEARCH_TERM', 'ISSUER_NAME', 'FILING_PERSON', 'ADDRESS', 'DOCUMENT_NAME', 'DOCUMENT_TYPE'])
        writer.writeheader()
        for issuer in issuers:
            #print "ISSUER: " + issuer
            filing_person = issuer[IssuerQueries.FILING_PERSON_INDEX]
            print "---FILING PERSON: %s" % filing_person
            address = find_address(con, filing_person)

            row = {}
            row['CUSIP6'] = issuer[IssuerQueries.CUSIP_INDEX]
            row['SEARCH_TERM'] = issuer[IssuerQueries.SEARCH_TERM_INDEX]
            row['ISSUER_NAME'] = issuer[IssuerQueries.ISSUER_NAME_INDEX]
            row['FILING_PERSON'] = issuer[IssuerQueries.FILING_PERSON_INDEX]
            row['ADDRESS'] = address
            row['DOCUMENT_NAME'] = issuer[IssuerQueries.DOCUMENT_NAME_INDEX]
            row['DOCUMENT_TYPE'] = issuer[IssuerQueries.DOCUMENT_TYPE_INDEX]
            writer.writerow(row)
