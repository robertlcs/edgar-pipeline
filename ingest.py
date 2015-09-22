from subprocess import call, Popen, PIPE, STDOUT

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

    cmd = "cat sql/import-processed-items.sql | sqlite3 ingest.db"
    ps = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    (output, err_output) = ps.communicate()
    print output
    print err_output

if __name__ == "__main__":
    ingest()

