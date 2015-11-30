import argparse

from subprocess import call, Popen, PIPE, STDOUT
import csv
import sqlite3 as lite
import os

# See: http://stackoverflow.com/a/26193552/479490

def emit_unicode_string(value):
    try:
        return unicode(value, 'utf-8')
    except UnicodeDecodeError:
        return unicode(value, 'iso-8859-1')

def unicode_csv_reader(csv_file, dialect=csv.excel, **kwargs):
    csv_reader = csv.DictReader(csv_file, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield {key: emit_unicode_string(row[key]) for key in row.keys()}

def ingest(path, incremental=False):
    if not incremental:
        cmd = "cat sql/create.sql | sqlite3 ingest.db"
        ps = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        (output, err_output) = ps.communicate()
        print output
        print err_output

        cmd = "cat sql/init-sp500.sql | sqlite3 ingest.db"
        ps = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        (output, err_output) = ps.communicate()
        print output
        print err_output

    con = lite.connect("ingest.db")
    with con:

        # Valid items
        con.execute("DROP TABLE IF EXISTS tmp_valid_items")

        stmt = '''CREATE TABLE tmp_valid_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           search_company VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           score NUMERIC NOT NULL)'''
        con.execute(stmt)

        with open(os.path.join(path, "valid-items.csv"), "r") as valid_items_csv:
            reader = unicode_csv_reader(valid_items_csv)
            for row in reader:
                stmt = '''INSERT INTO tmp_valid_items (cusip, url, address, search_company, issue_name, issuer_name, document_name, date, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row.get('search_company'), row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['score'],))

        stmt = "INSERT INTO valid_items(cusip, url, address, search_company, issue_name, issuer_name, document_name, date, score) SELECT cusip, url, address, search_company, issue_name, issuer_name, document_name, date, score FROM tmp_valid_items"
        con.execute(stmt)
        con.execute("DROP TABLE tmp_valid_items")

        # Rejected items
        con.execute("DROP TABLE IF EXISTS tmp_rejected_items")

        stmt = '''CREATE TABLE tmp_rejected_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           search_company VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           validation_reason VARCHAR)'''
        con.execute(stmt)

        with open(os.path.join(path, "rejected-items.csv"), "r") as rejected_items_csv:
            reader = unicode_csv_reader(rejected_items_csv)
            for row in reader:
                stmt = 'INSERT INTO tmp_rejected_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row.get('search_company'), row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['validation_reason']))

        stmt = "INSERT INTO rejected_items(cusip, url, address, search_company, issue_name, issuer_name, document_name, date, validation_reason) SELECT cusip, url, address, search_company, issue_name, issuer_name, document_name, date, validation_reason FROM tmp_rejected_items"
        con.execute(stmt)
        con.execute("DROP TABLE tmp_rejected_items")

        # Duplicate items
        stmt = '''CREATE TABLE tmp_duplicate_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           search_company VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           score NUMERIC NOT NULL)'''
        con.execute(stmt)

        with open(os.path.join(path, "duplicate-items.csv"), "r") as duplicate_items_csv:
            reader = unicode_csv_reader(duplicate_items_csv)
            for row in reader:
                print row

                stmt = 'INSERT INTO tmp_duplicate_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row.get('search_company'), row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['score']))

        stmt = "INSERT INTO duplicate_items(cusip, url, address, search_company, issue_name, issuer_name, document_name, date, score) SELECT cusip, url, address, search_company, issue_name, issuer_name, document_name, date, score FROM tmp_duplicate_items"
        con.execute(stmt)
        con.execute("DROP TABLE tmp_duplicate_items")

    # Select into the valid_items, rejected_items and duplicate items tables

    # Delete temp tables


#    cmd = "cat sql/import-processed-items.sql | sqlite3 ingest.db"
#    ps = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
#    (output, err_output) = ps.communicate()
#    print output
#    print err_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process crawled items.')
    parser.add_argument("-i",
                    "--incremental",
                    action="store_true",
                    help="this is an incremental ingest, so don't drop/create the database.")
    parser.add_argument("path",
                        help="path to processed files (directory)",
                        default="processed-data")
    args = parser.parse_args()

    ingest(args.path, args.incremental)

