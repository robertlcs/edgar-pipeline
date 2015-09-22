from commandline import execute_command

import argparse
import codecs
import csv
import re
import sqlite3 as lite
import sys

def gen_target_path(path):
    m = re.match("(.*)\.csv$", path)
    if m:
        base = m.group(1)
    else:
        print "Please input a csv path"
        sys.exit(-1)
    return base + "_mapped.csv"

parser = argparse.ArgumentParser(description='Process batch items.')
parser.add_argument("source", nargs="+", help="Path to AMT batch results file")
args = parser.parse_args()

source_paths = args.source
source_to_target_paths = dict()
for source_path in source_paths:
    source_to_target_paths[source_path] = gen_target_path(source_path)

fields = ['cusip', 'url', 'document_name', 'issuer_name', 'issue_name', 'address']
for source_path in source_paths:
    with open(source_path, "rU") as source_csv:
        reader = csv.DictReader(source_csv)
        target_path = source_to_target_paths[source_path]
        print "Writing temp file to %s" % target_path
        with open(target_path, "w") as target_csv:
            writer = csv.DictWriter(target_csv, fields)
            writer.writeheader()
            for row in reader:
                output_row = dict()
                output_row['cusip'] = row['Answer.cusip_numbers']
                output_row['url'] = row['Input.url']
                output_row['document_name'] = row['Input.document_name']
                output_row['address'] = row['Answer.issuer_address']
                output_row['issuer_name'] = row['Answer.issuer_name']
                output_row['issue_name'] = row['Answer.issue_names']
                writer.writerow(output_row)

        #cmd = "echo -e '.mode csv\\n.import %s amt_batch_items' | sqlite3 ingest.db" % target_path
        #execute_command(cmd)

        with lite.connect('ingest.db') as con:
            con.text_factory=str
            with open(target_path, "r") as target_csv:
                reader = csv.DictReader(target_csv)
                rows = [(row['cusip'], row['url'], row['document_name'], row['issuer_name'], row['issue_name'], row['address']) for row in reader]
                con.executemany("INSERT INTO amt_batch_items VALUES(?, ?, ?, ?, ?, ?)",
                                rows)

print "Fetching joined tables..."
fields += ['date']
print "Fields: "
print fields

with lite.connect('ingest.db') as con:
    con.text_factory = str
    with open("amt_batch_items.csv", "w") as output_csv:
        writer = csv.DictWriter(output_csv, fields)
        writer.writeheader()
        cur = con.cursor()
        cur.execute("select a.cusip, a.url, a.address, a.issuer_name, a.issue_name, a.document_name, b.date " \
                    "from amt_batch_items as a, rejected_items as b where a.url = b.url;")
        results = cur.fetchall()
        #print results

        if results:
            for row in results:
                #print row
                output_row = dict()
                output_row['cusip'] = row[0]
                output_row['url'] = row[1]
                output_row['address'] = row[2]
                output_row['issuer_name'] = row[3]
                output_row['issue_name'] = row[4]
                output_row['document_name'] = row[5]
                output_row['date'] = row[6]
                writer.writerow(output_row)
        else:
            print "No results."
