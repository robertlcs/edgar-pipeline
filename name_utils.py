import re


def escape_name(company_name):
    company_name = company_name.replace("'", "")
    company_name = re.sub(r'\bAND\b', '', company_name)
    company_name = re.sub(r'\s+', ' ', company_name)
    return company_name

def is_parent_company(company_name, issuer_name):
    if company_name == issuer_name:
        return True

    company_name = escape_name(company_name)

    #print "Company name: " + company_name

    pat = "%s\s*(CA|CO|DE|CO DE|INC|NY|NV|N V|OH|CO NEW|NEW|MD|MA|MN|TX|MI|OH|NW){0,1}$" % company_name

#    print "Pattern: " + pat
#    print "Issuer name: " + issuer_name

    if re.match(pat, issuer_name):
##        print "Matches"
        return True
 #

    return False

