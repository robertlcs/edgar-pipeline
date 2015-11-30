import re

def get_stem_of_company_name(name):
    # Get rid of punctuation
    name = name.replace('.', '')
    name = name.replace('-', ' ')
    name = name.replace('!', ' ')
    name = name.replace('&', ' ')
    name = name.replace("'", '') # Replace with no space

    words_to_remove = ['GROUP', 'INC', 'DE', 'CORP', 'CO', 'COMPANY', 'LTD', 'NV', 'LIMITED', 'PLC', 'SYSTEMS',
                       'SYSTEM', 'RESOURCE', 'RESOURCES', 'PLC', 'INTERNATIONAL', 'MARKET', 'HOLDINGS', 'COMPANIES',
                       'AND', 'DE', 'NY', 'MN', 'NV', 'N V'
                       ]
    pats = [r'\b%s\b' % word for word in words_to_remove]
    for pat in pats:
        name = re.sub(pat, '', name, re.IGNORECASE)
    name = re.sub('\s+', ' ', name).strip()

    #print "Stem: %s " % name
    return name

def get_db_name_pattern(name):
    name = get_stem_of_company_name(name)
    name = name.replace(' ', '%')
    return name + '%'

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

