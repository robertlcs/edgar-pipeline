from prettytable import PrettyTable
import sqlite3 as lite
import sys

def usage():
    print "Usage: python gen_sp500_report.py <format>"

if len(sys.argv) > 1:
    format = sys.argv[1]
else:
    format = "text"

con = lite.connect('ingest.db')

col_names = ['Company Name', 'Number of Issues', 'Number of Common Stocks', 'Number of Notes']
pt = PrettyTable(col_names)

with con:
    cur = con.cursor()
    cur.execute("select company from sp500_companies")
    rows = cur.fetchall()
    companies = [row[0] for row in rows]
    companies.sort()

    for company in companies:
        cur.execute("select count(*) from valid_items where issuer_name = :CompanyName",
                    {'CompanyName' : company})
        row = cur.fetchone()
        num_issues = row[0]

        cur.execute("select count(*) from valid_items where issuer_name = :CompanyName and upper(issue_name) like '%Common%'",
                    {'CompanyName' : company})
        row = cur.fetchone()
        num_common_stocks = row[0]

        cur.execute("select count(*) from valid_items where issuer_name = :CompanyName and upper(issue_name) like '%Notes%'",
                    {'CompanyName' : company})
        row = cur.fetchone()
        num_notes = row[0]

        #print "%s, %s, %s, %s" % (company, num_issues, num_common_stocks, num_notes)

        row = (company, num_issues, num_common_stocks, num_notes)
        pt.add_row(row)

if format == 'html':
    contents = pt.get_html_string()
    ext = "html"
else:
    contents = pt.get_string()
    ext = "txt"

output = open("reports/sp500_companies.%s" % ext, "w")
output.write(contents)
output.close()

