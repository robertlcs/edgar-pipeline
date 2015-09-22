from decimal import Decimal
import csv
import sqlite3 as lite
import os

sp500_count = 502

def pretty_print_row(row):
    for key in row.keys():
        print "%s: %s" % (key, row[key])

con = lite.connect('ingest.db')

with con:
    cur = con.cursor()
    cur.execute('select count(*) from sp500_companies where company not in (select distinct issuer_name from valid_items);')
    missing_count = cur.fetchone()[0]

    cur.execute("select count(*) from valid_items where issuer_name in (select company from sp500_companies)")
    num_issues_for_sp500_companies = cur.fetchone()[0]

    cur.execute("select count(*) from valid_items where upper(issue_name) like '%COMMON%'")
    num_common_stocks = cur.fetchone()[0]

    cur.execute("select count(*) from valid_items where upper(issue_name) like '%COMMON%' and issuer_name in (select company from sp500_companies)")
    num_common_stocks_for_sp500_companies = cur.fetchone()[0]

    TWOPLACES = Decimal(10) ** -2
    percent_sp500_with_common_stocks = Decimal(num_common_stocks_for_sp500_companies) / Decimal(sp500_count)
    percent_sp500_with_common_stocks = percent_sp500_with_common_stocks.quantize(TWOPLACES)

    cur.execute("select count(distinct(issuer_name)) from valid_items")
    issuer_count = cur.fetchone()[0]

    cur.execute("select count(distinct(cusip)) from valid_items")
    cusip_count = cur.fetchone()[0]

    cur.execute("select count(*) from valid_items")
    valid_count = cur.fetchone()[0]

    cur.execute('select count(*) from rejected_items')
    rejected_count = cur.fetchone()[0]

    cur.execute('select count(*) from duplicate_items')
    duplicate_count = cur.fetchone()[0]

    total_count = rejected_count + valid_count + duplicate_count
    percent_accepted = Decimal(Decimal(valid_count) / Decimal(total_count)).quantize(TWOPLACES)

fields = ['Search Size', 'Total Num Documents', 'Num Common Stocks for Search Set', 'Percent (%) Coverage of Common Stocks', 'Total Num Common Stocks', 'Total Num Issuers', 'Total Num CUSIP', 'Num Rejected', 'Num Duplicates', 'Percent (%) Accepted']
with open("metrics.csv", "w") as output_csv:
    writer = csv.DictWriter(output_csv, fields)
    writer.writeheader()
    row = {
        'Search Size' : sp500_count,
        'Total Num Documents' : total_count,
        'Num Common Stocks for Search Set' : num_common_stocks_for_sp500_companies,
        'Percent (%) Coverage of Common Stocks' : percent_sp500_with_common_stocks,
        'Total Num Common Stocks' : num_common_stocks,
        'Total Num Issuers' : issuer_count,
        'Total Num CUSIP' : cusip_count,
        'Num Rejected' : rejected_count,
        'Num Duplicates' : duplicate_count,
        'Percent (%) Accepted' : percent_accepted }

    print "----- Crawl results -----"
    print "# items crawled: %s" % total_count
    print "# items valid: %s" % valid_count
    print "# items rejected: %s" % rejected_count
    print "# items duplicates: %s" % duplicate_count
    print "Percentage accepted (valid): %s" % percent_accepted
    print

    print "------------ Stocks and Bonds ------------"
    print "Number of common stocks: %s" % num_common_stocks
    print "Number of issues (CUSIP's): %s" % cusip_count
    print

    print "---------- S&P 500 Index -----------"
    print "# of common stocks for SP500: %s" % num_common_stocks_for_sp500_companies
    print "# of companies in index: %s" % sp500_count
    print "Percentage of S&P 500 common stocks found/accepted: %s" % percent_sp500_with_common_stocks

    writer.writerow(row)








