import csv
from decimal import Decimal
import sys
import sqlite3 as lite
from name_resolution import get_db_name_pattern
from company_queries import get_companies

TWOPLACES = Decimal(10) ** -2

def find_possible_issuers(con, log_file, company):
    cur = con.cursor()
    pat = get_db_name_pattern(company)
    query = "select issuer_name from master_issuers where issuer_name like '%s'" % pat
    log_query(query, log_file)

    cur.execute("select issuer_name from master_issuers where issuer_name like ?", [pat])
    results = cur.fetchall()
    return [row[0] for row in results]

def fetch_count(con, query, bindings=None):
    cur = con.cursor()
    if bindings:
        cur.execute(query, bindings)
    else:
        cur.execute(query)
    row = cur.fetchone()
    return row[0]

def log_query(query, f):
    f.write(query + "\n")

con = lite.connect('ingest.db')
with con:

    print "Valid, duplicate and rejected counts"
    print "------------------------------------"
    valid_items_count = fetch_count(con, "select count(*) from valid_items")
    rejected_items_count = fetch_count(con, "select count(*) from rejected_items")
    duplicate_items_count = fetch_count(con, "select count(*) from duplicate_items")

    print "# valid: " + str(valid_items_count)
    print "# rejected: " + str(rejected_items_count)
    print "# duplicate: " + str(duplicate_items_count)
    print "TOTAL # CRAWLED: " + str(valid_items_count + duplicate_items_count + rejected_items_count)

    # extract issuers (cusip6's) from valid_items
    crawled_issuers_count = fetch_count(con, "select count(distinct substr(cusip, 1, 6)) from valid_items")
    print "# distinct valid issuers (CUSIP6's): " + str(crawled_issuers_count)

    cur = con.cursor()
    cur.execute("select validation_reason, count(validation_reason) from rejected_items group by validation_reason")
    rejection_counts = {}
    for row in cur.fetchall():
        rejection_counts[row[0]] = row[1]

    for reason in rejection_counts.keys():
        print "# rejected for '%s': %d" % (reason, rejection_counts[reason])

    # compare count against master file
    companies = get_companies(con)
    master_issuers_count = 0
    companies_coverage = {}

    print "Generating master issuer coverage stats..."
    query_log_file = open("queries.txt", "w")

    missing_companies = []
    with query_log_file:
        for company in companies:

            possible_issuers = find_possible_issuers(con, query_log_file, company)
            master_issuers_count += len(possible_issuers)

            crawled_issuers_for_company_count = fetch_count(con,
                                                            '''select count(distinct substr(cusip, 1, 6))
                                                            from valid_items
                                                            where issuer_name like ?''',
                                                            [get_db_name_pattern(company)])
            company_master_issuers_count = len(possible_issuers)

            if company_master_issuers_count > 0:
                percentage_issuers_crawled_for_company = Decimal(100) * Decimal(crawled_issuers_for_company_count) / Decimal(company_master_issuers_count)
                percentage_issuers_crawled_for_company = percentage_issuers_crawled_for_company.quantize(TWOPLACES)
            else:
                percentage_issuers_crawled_for_company = "NaN"
                missing_companies.append(company)

            companies_coverage[company] = {'CRAWLED_ISSUERS_COUNT' : crawled_issuers_for_company_count,
                                           'MASTER_ISSUERS_COUNT' : company_master_issuers_count,
                                           'COVERAGE (%)' : percentage_issuers_crawled_for_company}

            #print "%s: %d of %d issuer numbers crawled. Coverage: %s"  % (company,
            #                                                              crawled_issuers_for_company_count,
            #                                                              company_master_issuers_count,
            #                                                              percentage_issuers_crawled_for_company)

print "Stats generated, writing..."

fields = ['COMPANY', 'CRAWLED_ISSUERS_COUNT', 'MASTER_ISSUERS_COUNT', 'COVERAGE (%)']
with open('coverage_metrics.csv', 'w') as coverage_metrics_csv:
    writer = csv.DictWriter(coverage_metrics_csv, fields)
    writer.writeheader()
    for company in companies:
        row = companies_coverage[company]
        row['COMPANY'] = company
        writer.writerow(row)

print "Wrote to coverage_metrics.csv"

fields = ['COMPANY', 'ISSUER']
with open("missing_issuers.csv", "w") as missing_issuers_csv:
    writer = csv.DictWriter(missing_issuers_csv, fields)
    writer.writeheader()
    for company in missing_companies:
        row = {}
        row['COMPANY'] = company
        writer.writerow(row)

print "Missing issuers are found in missing_issuers.csv"
