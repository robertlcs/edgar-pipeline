import re
from name_resolution import get_stem_of_company_name

def clean_issuer_name(issue_name):
    m = re.match(r'"(.*)"', issue_name)
    if m:
        issue_name = m.group(1)

    cleaned_issuer_name = issue_name.upper().strip()
    if re.search(r'CORPORATION', issue_name, re.IGNORECASE):
        cleaned_issuer_name = cleaned_issuer_name.replace('CORPORATION', 'CORP')

    m = re.match(r'(.*) CLASS [A-Z]$', cleaned_issuer_name)
    if m:
        cleaned_issuer_name = m.group(1)

    m = re.match(r'(.*)&*\s*COMPANY$', cleaned_issuer_name)
    if m and m.group(1):
        cleaned_issuer_name = m.group(1)

    m = re.match(r'(.*) INCORPORATED$', cleaned_issuer_name)
    if m:
        cleaned_issuer_name = m.group(1) + " INC"

    m = re.match(r'(.*) & CO\.(.*)$', cleaned_issuer_name)
    if m:
        cleaned_issuer_name = m.group(1) + m.group(2)

    cleaned_issuer_name = cleaned_issuer_name.replace('-', ' ')
    cleaned_issuer_name = cleaned_issuer_name.replace('&', ' ')
    cleaned_issuer_name = cleaned_issuer_name.replace('.', ' ')
    cleaned_issuer_name = cleaned_issuer_name.replace('!', ' ')

    cleaned_issuer_name = re.sub('\s+', ' ', cleaned_issuer_name).strip()
    return cleaned_issuer_name

# Like clean, but removes any modifiers, suffixes, etc., to get the root company name
def strip_issuer_name(issuer_name):
    return get_stem_of_company_name(issuer_name)

def clean_cusips(item):
    cleaned_cusips = []

    if item.get('cusip'):
        cusips = item['cusip']
        cusips = cusips.replace(",", ";")
        cusips = cusips.split(";")
        for cusip in cusips:
            cusip = cusip.replace("-", "")
            cusip = cusip.replace(" ", "")
            cusip = cusip.replace("#", "")
            cleaned_cusips.append(cusip)
        item['cusip'] = "; ".join(cleaned_cusips)

    return cleaned_cusips

def clean_item(item):

    address = item.get('address')
    if address:
        item['address'] = clean_address(address)

    cusips = clean_cusips(item)

    # Clean issuer name
    if item.get('issuer_name'):
        item['issuer_name'] = clean_issuer_name(item['issuer_name'])

def clean_address(address):
    address = address.strip()
    address = re.sub(',+', ',', address)

    if len(address) > 75:
      
        # Check for "... Item 2,"
        match = re.search(r'(.*?),\s+Item 2', address, flags=re.IGNORECASE)
        if match:
            address = match.group(1).strip()

        # Check for "... offices are located at " pattern
        match = re.search("offices*\ (of the Company )*(are|is) located at,*\s+(.*)", address, flags=re.IGNORECASE)
        if match:
            address = match.group(3).strip()

        match = re.search("offices* (are|is):*\s*(.*)", address, flags=re.IGNORECASE)
        if match:
            address = match.group(2).strip()

        # Check for dashed line ending
        match = re.search('(-+$)', address)
        if match:
            address = address.replace(match.group(1), "").strip()
        match = re.search("Address,*\s+of\s+Issuer'*\s*s\s+Principal\s+Executive\s+Offices(.*)", address, flags=re.IGNORECASE)

        # Remove redundant "Address of Issuer's..."
        if match:
            address = match.group(1).strip()

        # Remove any beginning or ending punctuation
        match = re.search('^[,\.;]*\s*(.*?)[,\.;]*$', address)
        if match:
            address = match.group(1).strip()

    return address