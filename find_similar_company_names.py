import argparse
import csv
import sqlite3
import sys
from name_utils import is_parent_company

parser = argparse.ArgumentParser(description='Find similar issuer names.')
parser.add_argument("-e",
                    "--exclude",
                    action="store_true",
                    help="exclude exact matches if you only want to see issuers with multiple similar names")
#parser.add_argument("-w",
#                    "--write",
#                    action="store_true",
#                    help="write possible company name matches to output file")
parser.add_argument("-p",
                    "--parents",
                    action="store_true",
                    help="only output issuer names that could be parent companies")

args = parser.parse_args()

company_names = []
with open("sp500_companies_cleaned.csv", "r") as companies_csv:
    reader = csv.reader(companies_csv)
    for row in reader:
        company_names.append(row[0].rstrip())

EXACT_MATCH_QUERY_TEMPLATE = "select distinct issuer_name from %s where issuer_name = ? "\
                             "and (upper(issue_name) like '%%COMMON%%' or upper(issue_name) like '%%ORDINARY SHARES%%')"

SIMILAR_QUERY_TEMPLATE = "select distinct issuer_name from %s where issuer_name like ? and issuer_name != ? "\
                         "and (upper(issue_name) like '%%COMMON%%' or upper(issue_name) like '%%ORDINARY SHARES%%')"

def update_companies_to_issuers(name, issuer_name):
    issuers = companies_to_issuers.get(name)
    if not issuers:
        issuers = []
    issuers.append(issuer_name)
    companies_to_issuers[name] = issuers

def count_matching_issues_for_company(name, table):
    cur.execute(EXACT_MATCH_QUERY_TEMPLATE % table, [name])
    results = cur.fetchall()
    count = 0
    for item in results:
        issuer_name = item[0]
        update_companies_to_issuers(name, issuer_name)
        count += 1
    return count

def count_matching_valid_issuers_for_company(name):
    return count_matching_issues_for_company(name, "valid_items")

def count_matching_rejected_issuers_for_company(name):
    return count_matching_issues_for_company(name, "rejected_items")

def count_similar_issues_for_company(name, table):
    cur.execute(SIMILAR_QUERY_TEMPLATE % table, ['%' + name + '%', name])
    results = cur.fetchall()
    count = 0
    for item in results:
        issuer_name = item[0]
        update_companies_to_issuers(name, issuer_name)
        count += 1
    return count

def count_similar_valid_issuers_for_company(name):
    return count_similar_issues_for_company(name, "valid_items")

def count_similar_rejected_issuers_for_company(name):
    return count_similar_issues_for_company(name, "rejected_items")

companies_to_issuers = {}
same_count = 0
similar_count = 0

for name in company_names:
    con = sqlite3.connect("ingest.db")
    with con:
        cur = con.cursor()

        same_count += count_matching_valid_issuers_for_company(name)
        same_count += count_matching_rejected_issuers_for_company(name)

        similar_count += count_similar_rejected_issuers_for_company(name)
        similar_count += count_similar_rejected_issuers_for_company(name)

print "%s same names" % same_count
print "%s similar but different names" % similar_count
print "Companies to issuer names:"
with open("companies_to_issuers.csv", "w") as csv_output:
    writer = csv.DictWriter(csv_output, ['COMPANY', 'ISSUER'])
    writer.writeheader()
    company_names = companies_to_issuers.keys()
    company_names.sort()
    for name in company_names:
        issuers = list(set(companies_to_issuers[name]))
        issuers.sort()
        has_different_names = ([issuer != name for issuer in issuers]).count(True) > 0
        if not args.exclude or has_different_names:
            print name
            for issuer in issuers:
                print "\t%s (Parent Co? %s)" % (issuer, "Y" if is_parent_company(name, issuer) else "N")
                if not args.parents or is_parent_company(name, issuer):
                    row = {}
                    row['COMPANY'] = name
                    row['ISSUER'] = issuer
                    writer.writerow(row)

print "Wrote to companies_to_issuers.csv."
