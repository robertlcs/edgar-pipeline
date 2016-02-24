import csv
import re
import sqlite3 as lite

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def get_issues(con, cik):
    query = "select cusip, issuer_name, issue_name from valid_items where search_term='%s'" % cik
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    issues = []
    for row in results:
        issue = Bunch(cusip = row[0], issuer_name = row[1], issue_name = row[2])
        issues.append(issue)
    return issues

stats = {}
missing_common = []

with open("russell_2000_cik_to_ticker.csv") as ciks_in:
    reader = csv.DictReader(ciks_in)
    con = lite.connect('ingest.db')
    with con:
        for row in reader:
            cik = row['CIK']
            if not cik:
                print "Missing CIK for %s (%s) " % (row['Name'], row['Ticker'])
                continue
            issues = get_issues(con, cik)
            common = filter(lambda x: re.search(r'Common', x.issue_name, flags=re.IGNORECASE), issues)
            issuer_names = list(set(map(lambda x: x.issuer_name, issues)))
            stats[cik] = {'cik' : cik, 'issuer_names' : ','.join(issuer_names), 'num_issues' : len(issues), 'num_common' : len(common)}
            if len(common) == 0:
                missing_common.append(cik)

with open("russell_2000_stats.csv", "w") as out_csv:
    writer = csv.DictWriter(out_csv, ['cik', 'issuer_names', 'num_issues', 'num_common'])
    writer.writeheader()
    for cik in stats.keys():
        writer.writerow(stats[cik])

with open("russell_2000_missing.csv", "w") as out_csv:
    writer = csv.writer(out_csv)
    for cik in missing_common:
        writer.writerow([cik])

