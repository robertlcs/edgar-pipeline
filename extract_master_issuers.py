import argparse
import csv
import re
import sys

parser = argparse.ArgumentParser(description="Extract issuers from master file")
parser.add_argument("master_file", help="Path to master file")
args = parser.parse_args()

with open(args.master_file, "rU") as master_file_csv:
    reader = csv.reader(master_file_csv, delimiter="|")
    writer = csv.DictWriter(sys.stdout, fieldnames = ['CUSIP6', 'ISSUER'])
    writer.writeheader()
    for row in reader:
        out_row = {}
        #print row
        if len(row) > 1 and row[0] != '999999' and not re.match('^RESERVED', row[2]):
            out_row['CUSIP6'] = row[0].strip()
            out_row['ISSUER'] = row[2].strip()
            writer.writerow(out_row)

