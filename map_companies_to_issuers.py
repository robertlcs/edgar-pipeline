import argparse
import csv
import re
import sqlite3

parser = argparse.ArgumentParser(description="Map companies to issuers")
parser.add_argument("companies", help="List of companies to map")
args = parser.parse_args()

def get_root(company):
    company = company.replace('.', '')
    re.match()

def find_possible_issuers(con, company):
    company = get_root(company)
    cur = con.cursor()
    cur.execute("select issuer_name from master_issuers where issuer_name like ?", ['%' + company + '%'])
    results = cur.fetchall()
    return [row[0] for row in results]

with open(args.companies, "r") as in_csv:
    reader = csv.DictReader(in_csv)
    con = sqlite3.connect("ingest.db")
    with con:
        for row in reader:
            company = row['COMPANY']
            candidates = find_possible_issuers(con, company)
            if len(candidates) == 0:
                print "No matches for %s" % company
                continue

            if len(candidates) > 1:
                print "Multiple possible issuers for %s: " % company
                for candidate in candidates:
                    print "\t%s" % candidate

            print candidates[0]


