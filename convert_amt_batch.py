import csv
import sys

def usage():
    print "Usage: python convert_amt_batch.py <source>"

if len(sys.argv) < 2:
    print usage()
    sys.exit(-1)

path = sys.argv[1]

fields = ['cusip', 'url', 'document_name', 'issuer_name', 'issue_name', 'address']
with open(path, "rU") as source_csv:
    reader = csv.DictReader(source_csv)
    writer = csv.DictWriter(sys.stdout, fields)
    #writer.writeheader()
    for row in reader:
        output_row = dict()
        output_row['cusip'] = row['Answer.cusip_numbers']
        output_row['url'] = row['Input.url']
        output_row['document_name'] = row['Input.document_name']
        output_row['address'] = row['Answer.issuer_address']
        output_row['issuer_name'] = row['Answer.issuer_name']
        writer.writerow(output_row)
