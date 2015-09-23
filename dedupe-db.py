import sqlite3
con = sqlite3.connect("ingest.db")
with con:
    cur = con.cursor()
    cur.execute("select cusip from valid_items group by cusip having count(*) > 1;")
    cusips = cur.fetchall()
    num_rows_deleted = 0

    for cusip in cusips:
        cusip = cusip[0]
        print cusip

        cur.execute("select id from valid_items where cusip = ? order by score desc", (cusip,))
        items = cur.fetchall()
        if len(items) > 0:
            for item in items[1:]:
                num_rows_deleted += cur.execute("delete from valid_items where id=?", (item[0],)).rowcount

    print "%d cusips found with duplicate rows" % len(cusips)
    print "%d rows deleted" % num_rows_deleted





