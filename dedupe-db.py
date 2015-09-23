import sqlite3
con = sqlite3.connect("ingest.db")
with con:
    cur = con.cursor()
    cur.execute("select cusip from valid_items group by cusip having count(*) > 1;")
    cusips = cur.fetchall()
    for cusip in cusips:
            cusip = cusip[0]
            print cusip

            cur.execute("select * from valid_items where cusip = ? order by score descending;")
            items = cur.fetchall()
            if len(items) > 0:
                for item in items[1:]:




