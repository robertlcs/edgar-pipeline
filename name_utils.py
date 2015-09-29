import re


def escape_name(company_name):
    company_name = company_name.replace("'", "")
    company_name = company_name.replace("AND", "")
    company_name = re.sub(r'\s+', ' ', company_name)
    return company_name

def is_parent_company(company_name, issuer_name):
    company_name = escape_name(company_name)

#    print company_name

    pat = "%s\s*(CO|DE|CO DE|INC|NY|NV|N V|OH|CO NEW|NEW|MD|MA){0,1}$" % company_name

#    print pat
#    print issuer_name

    if re.match(pat, issuer_name):
##        print "Matches"
        return True
 #

    return False

