# encoding=utf8
import argparse
import csv
import sys
import urllib
from geocoding.address import clean

reload(sys)
sys.setdefaultencoding('utf8')

path = "issuer-cusip6s.csv"

parser = argparse.ArgumentParser(prog="map_to_pcmgbi_match.py")
parser.add_argument("output", help="path to output")
parser.add_argument("input", help="path to input")
args = parser.parse_args()

# CUSIP6,CUSIP8,CHECKSUM,NAME,ADDRESS
CUSIP6 = 1
STREET = 11
CITY = 13
STATE = 14
POSTAL = 15
COMPANY_NAME = 9
COUNTRY = 17

print "Opening %s to read..." % args.input
print "Opening %s to output..." % args.output

with open(args.input, "r") as csv_in:
    reader = csv.DictReader(csv_in)
    with open(args.output, "w") as csv_out:
        writer = csv.writer(csv_out)
        for in_row in reader:
            out_row = [''] * 22
            addr = in_row['ADDRESS']
            if addr:
                print "Cleaning address..."
                print "Input: " + addr
                addr = clean(addr)
                if addr:
                    (street, city, state, postal, country) = addr
                    print "---- %s, %s, %s, %s, %s -----" % addr
                    out_row[STREET] = street if street else ''
                    out_row[CITY] = city if city else ''
                    out_row[STATE] = state if state else ''
                    out_row[POSTAL] = postal if postal else ''
                    out_row[COUNTRY] = country if country else ''
                else:
                    print "NO MATCHING ADDRESS"
            out_row[CUSIP6] = in_row['CUSIP6']
            out_row[COMPANY_NAME] = in_row['NAME']
            writer.writerow(out_row)
