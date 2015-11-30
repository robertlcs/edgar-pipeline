from geocoding.address import clean

import csv
import argparse
import sys

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Geocode csv file.')
parser.add_argument("path", help="Path to csv")
parser.add_argument("field", help="Name of address field")
args = parser.parse_args()

def read_fieldnames(path):
    with open(path, "r") as path_csv:
        reader = csv.reader(path_csv)
        row = reader.next()
        return row

fieldnames = read_fieldnames(args.path) + ['STREET', 'CITY', 'STATE', 'POSTAL', 'COUNTRY']
with open(args.path, "r") as path_csv:
    reader = csv.DictReader(path_csv)
    with open("geocoded.csv", "w") as geocoded_out:
        writer = csv.DictWriter(geocoded_out, fieldnames)
        for row in reader:
            address = row[args.field]
            print "Geocoding " + address
            geo_address = clean(address)
            if geo_address:
                (row['STREET'], row['CITY'], row['STATE'], row['POSTAL'], row['COUNTRY']) = geo_address
                writer.writerow(row)

