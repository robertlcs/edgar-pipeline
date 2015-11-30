import csv
import sqlite3 as lite

con = lite.connect("ingest.db")
with con:
    with open("issuers_scrape_results.csv") as input_csv:
        reader = csv.DictReader(input_csv)
        for row in reader:
            issuer_name = row['issuer_name']
            address = row['address']
            con.execute("update valid_items set address = ? where issuer_name = ?", [address, issuer_name])


