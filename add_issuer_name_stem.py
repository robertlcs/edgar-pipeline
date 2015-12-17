from cleaning import strip_issuer_name

import argparse
import csv
import os

def read_fieldnames(path):
    with open(path, "r") as path_csv:
        reader = csv.reader(path_csv)
        row = reader.next()
        return row

parser = argparse.ArgumentParser(description='Enrich file with issuer name stem.')
parser.add_argument("path", help="path to input file")
args = parser.parse_args()
fieldnames = read_fieldnames(args.path)

basename = os.path.basename(args.path)
(root, extension) = os.path.splitext(basename)

with open(args.path, "r") as path_csv:
    reader = csv.DictReader(path_csv)

    import re
    if re.search(r'_', root):
        separator = '_'
    else:
        separator = '-'

    with open(root + "%swith%sstems.csv" % (separator, separator), "w") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames + ['STEM'])
        writer.writeheader()
        for row in reader:
            row['STEM'] = strip_issuer_name(row['SEARCH_TERM'])
            writer.writerow(row)

