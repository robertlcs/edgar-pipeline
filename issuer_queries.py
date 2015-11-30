def old_get_issuers(con):
    cur = con.cursor()
    cur.execute("select distinct issuer_name from valid_items order by issuer_name asc")
    results = cur.fetchall()
    return [row[0] for row in results]

def get_issuers(con):
    cur = con.cursor()
    cur.execute("select distinct substr(cusip, 1, 6), search_company, issuer_name from valid_items order by search_company asc")
    results = cur.fetchall()
    return [(row[0], row[1], row[2]) for row in results]
