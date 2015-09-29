import csv
import sqlite3

# select issuer_name from valid_items where issuer_name like '%3M%';

company_names = []
with open("sp500_companies_cleaned.csv", "r") as companies_csv:
    reader = csv.reader(companies_csv)
    for row in reader:
        company_names.append(row[0])

company_names.sort()

different_count = 0
same_count = 0

print "company_name, issuer"
con = sqlite3.connect("ingest.db")

company_names_to_issuers = {}

def get_issuers_for_company_name(query, params):
    return [row[0] for row in cur.execute(query, params)]

def remove_duplicate_issuers(issuers):
    unique_issuers = []
    for issuer in issuers:
        if issuer not in unique_issuers:
            unique_issuers.append(issuer)
    return unique_issuers

for name in company_names:
    with con:
        cur = con.cursor()
        query = "select issuer_name from valid_items where issuer_name like ?"
        params = ['%' + name +'%']
        #cur.execute("select issuer_name from valid_items where issuer_name like ?", ['%' + name +'%'])
        #query = "select issuer_name from valid_items where issuer_name like '%%%s%%'" % escape(name)
        #print query
        valid_issuers = get_issuers_for_company_name(query, params)

        query = "select issuer_name from rejected_items where issuer_name like ?"
        params = ['%' + name + '%']

#        cur.execute("select issuer_name from rejected_items where issuer_name like ?", ['%' + name + '%'])
        #query = "select issuer_name from rejected_items where issuer_name like '%%%s%%'" % escape(name)
        #print query
        rejected_issuers = get_issuers_for_company_name(query, params)

        issuers = remove_duplicate_issuers(valid_issuers + rejected_issuers)
        for issuer in issuers:
            print "%s,%s" % (name, issuer)

