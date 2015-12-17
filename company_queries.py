# This method returns the cleaned companies in the database
def get_companies(con):
    cur = con.cursor()
    cur.execute("select company from sp500_companies order by company asc")
    results = cur.fetchall()
    return [row[0] for row in results]

def find_address(con, filing_person):
    cur = con.cursor()
    query = "select address from valid_items where filing_person = ? order by address desc limit 1"
    print query
    print filing_person

    cur.execute("select address from valid_items where filing_person = ? order by address desc limit 1", [filing_person])
    results = cur.fetchone()
    return results[0]

