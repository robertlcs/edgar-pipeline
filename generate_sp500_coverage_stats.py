from name_resolution import is_parent_company, escape_name

import csv
import sqlite3

# Script finds coverage of S&P 500 companies using the name of the company and a substring match
# of any issuer_name in valid_items. It also counts the number of rejected items for that issuer
# using the same pattern for issuer_name.

def db_escape_name(name):
    return name.replace("'", "%")

company_names = []
with open("sp500_companies_cleaned.csv", "r") as companies_csv:
    reader = csv.reader(companies_csv)
    for row in reader:
        company_names.append(row[0].rstrip())

companies_with_valid_or_rejected_issues = []
no_valid_common_stock_companies = []

query_template = "select issuer_name from %s where upper(issuer_name) like ? and (upper(issue_name) like '%%COMMON%%' or upper(issue_name) like '%%ORDINARY SHARES%%')"
print query_template
con = sqlite3.connect("ingest.db")
cur = con.cursor()

valid_common_stocks_count = 0
for name in company_names:
    #print name
    query = query_template % 'valid_items'
    cur.execute(query, ['%' + db_escape_name(escape_name(name)) + '%'])
    #print "Looking for valid issue name: " + db_escape_name(escape_name(name))
    items = cur.fetchall()

    has_common_stock = False

    for item in items:
        if is_parent_company(name, item[0]):
            has_common_stock = True
            break
        else:
            print "Comparing %s with %s" % (name, item[0])
            print "NOT MATCH!!!"
    if not has_common_stock:
        no_valid_common_stock_companies.append(name)
    else:
        companies_with_valid_or_rejected_issues.append(name)
        valid_common_stocks_count += 1

    if len(items) == 0:
        print "NO VALID ITEMS FOR %s" % name

print "# of companies with no valid common stock filings: %d" % len(no_valid_common_stock_companies)

# Are these companies with no valid common stock filings found in Common Stock filings in the rejected items table?
missing_common_stock_companies = []
count_not_found = 0
for name in no_valid_common_stock_companies:
    print name
    query = query_template % 'rejected_items'
    #print "Looking for rejected issue name: " + db_escape_name(escape_name(name))

    cur.execute(query, ['%' + db_escape_name(escape_name(name)) + '%'])
    items = cur.fetchall()

    has_common_stock = False

    for item in items:
        if is_parent_company(name, item[0]):
            has_common_stock = True
            break
        else:
            print "Comparing %s with %s: " % (name, item[0])
            print "NOT MATCH!!!"

    if not has_common_stock:
        missing_common_stock_companies.append(name)
    else:
        companies_with_valid_or_rejected_issues.append(name)

    if len(items) == 0:
        print "NO REJECTED ITEMS FOR %s" % name

print "# of companies with no valid or rejected common stock filings: %d" % len(missing_common_stock_companies)
print "Writing missing companies to missing-sp500-companies.csv..."

with open("missing-sp500-companies.csv", "w") as missing_out:
    for name in missing_common_stock_companies:
        missing_out.write(name + "\n")
        print name

print "Number of companies in S&P 500 with common stocks: %d" % valid_common_stocks_count
print "Percentage coverage: %d " % (100 * valid_common_stocks_count / len(company_names))




