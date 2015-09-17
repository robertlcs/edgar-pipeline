from subprocess import call, Popen, PIPE, STDOUT

import sys
import os

def ingest():
    cmd = "cat sql/create.sql | sqlite3 ingest.db"
    ps = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    (output, err_output) = ps.communicate()
    print output
    print err_output

    cmd = "cat sql/import-csv.sql | sqlite3 ingest.db"
    ps = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    (output, err_output) = ps.communicate()
    print output
    print err_output

ingest()
