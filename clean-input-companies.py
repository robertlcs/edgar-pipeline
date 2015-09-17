import csv
import re
import sys
from cleaning import clean_issuer_name

def usage():
    print "Usage: python clean-input-companies.py <file> <column=company_name>"

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]
if len(sys.argv) > 2:
    column = sys.argv[2]
else:
    column = "COMPANY"

with open(path, "r") as input_csv:
    reader = csv.reader(input_csv)
    headers = reader.next()

with open(path, "r") as input_csv:
    reader = csv.DictReader(input_csv)
    writer = csv.DictWriter(sys.stdout, headers, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for row in reader:
        company_name = clean_issuer_name(row[column])
        row[column] = company_name
        writer.writerow(row)



