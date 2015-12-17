class IssuerQueries():
    CUSIP_INDEX = 0
    SEARCH_TERM_INDEX = 1
    ISSUER_NAME_INDEX = 2
    FILING_PERSON_INDEX = 3
    DOCUMENT_NAME_INDEX = 4
    DOCUMENT_TYPE_INDEX = 5

    def old_get_issuers(con):
        cur = con.cursor()
        cur.execute("select distinct issuer_name from valid_items order by issuer_name asc")
        results = cur.fetchall()
        return [row[0] for row in results]

    @staticmethod
    def get_issuers(con):
        cur = con.cursor()
        cur.execute("select distinct substr(cusip, 1, 6), search_term, issuer_name, filing_person, document_name, "\
                    "document_type from valid_items order by issuer_name, filing_person asc")
        results = cur.fetchall()
        return [tuple(row[i] for i in range(6)) for row in results]
