from subprocess import call, Popen, PIPE, STDOUT
import csv
import sqlite3 as lite

def ingest(incremental=False):
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


    # I think we have to create temporary staging tables in order to
    # generate the autoincrement key

    con = lite.connect("ingest.db")
    with con:

        # Valid items
        stmt = '''CREATE TABLE tmp_valid_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           score NUMERIC NOT NULL)'''
        con.execute(stmt)

        with open("valid-items.csv", "r") as valid_items_csv:
            reader = csv.DictReader(valid_items_csv)
            for row in reader:
                stmt = 'INSERT INTO tmp_valid_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['score']))

        stmt = "INSERT INTO valid_items(cusip, url, address, issue_name, issuer_name, document_name, date, score) SELECT cusip, url, address, issue_name, issuer_name, document_name, date, score FROM tmp_valid_items"
        con.execute(stmt)
        con.execute("DROP TABLE tmp_valid_items")

        # Rejected items
        stmt = '''CREATE TABLE tmp_rejected_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           validation_reason VARCHAR)'''
        con.execute(stmt)

        with open("rejected-items.csv", "r") as valid_items_csv:
            reader = csv.DictReader(valid_items_csv)
            for row in reader:
                stmt = 'INSERT INTO tmp_rejected_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['validation_reason']))

        stmt = "INSERT INTO rejected_items(cusip, url, address, issue_name, issuer_name, document_name, date, validation_reason) SELECT cusip, url, address, issue_name, issuer_name, document_name, date, validation_reason FROM tmp_rejected_items"
        con.execute(stmt)
        con.execute("DROP TABLE tmp_rejected_items")

        # Duplicate items
        stmt = '''CREATE TABLE tmp_duplicate_items (
           cusip VARCHAR NOT NULL,
           url VARCHAR NOT NULL,
           address VARCHAR,
           issue_name VARCHAR,
           issuer_name VARCHAR,
           document_name VARCHAR,
           date DATE,
           score NUMERIC NOT NULL)'''
        con.execute(stmt)

        with open("duplicate-items.csv", "r") as duplicate_items_csv:
            reader = csv.DictReader(duplicate_items_csv)
            for row in reader:
                stmt = 'INSERT INTO tmp_duplicate_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                con.execute(stmt, (row['cusip'], row['url'], row['address'], row['issue_name'], row['issuer_name'], row['document_name'], row['date'], row['score']))

        stmt = "INSERT INTO duplicate_items(cusip, url, address, issue_name, issuer_name, document_name, date, score) SELECT cusip, url, address, issue_name, issuer_name, document_name, date, score FROM tmp_duplicate_items"
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
    ingest()

