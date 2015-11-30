__author__ = 'reedn'

import argparse
import csv

CUSIP6 = 1
STREET = 11
CITY = 13
STATE = 14
POSTAL = 15
COMPANY_NAME = 9
COUNTRY = 17

parser = argparse.ArgumentParser(prog="map_to_pcmgbi_match.py")
parser.add_argument("output", help="path to output")
parser.add_argument("input", help="path to input")
args = parser.parse_args()

fields = ['CUSIP6', 'COMPANY_NAME', 'STREET', 'CITY', 'STATE', 'POSTAL', 'COUNTRY']

with open(args.input, "r") as csv_in:
    with open(args.output, "w") as csv_out:
        reader = csv.reader(csv_in)
        writer = csv.DictWriter(csv_out, fields)
        writer.writeheader()
        for row in reader:
            output_row = {}
            output_row['CUSIP6'] = row[CUSIP6]
            output_row['STREET'] = row[STREET]
            output_row['CITY'] = row[CITY]
            output_row['STATE'] = row[STATE]
            output_row['POSTAL'] = row[POSTAL]
            output_row['COMPANY_NAME'] = row[COMPANY_NAME]
            output_row['COUNTRY'] = row[COUNTRY]
            writer.writerow(output_row)

