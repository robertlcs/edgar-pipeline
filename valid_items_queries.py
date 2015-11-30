def find_valid_items_for_issuer(con, issuer):
    cur = con.cursor()
    cur.execute('''select substr(cusip, 1, 6) as cusip6,
                substr(cusip, 7, 2) as cusip8,
                substr(cusip, 9, 1) as checksum
                from valid_items
                where issuer_name = ?''', [issuer])
    return cur.fetchall()

