import re

def clean_item(item):

    address = item.get('address')
    if address:
        item['address'] = clean_address(address)

    # Clean cusip #'s
    if item.get('cusip'):
        cusips = item['cusip'].split(";")
        cleaned_cusips = []
        for cusip in cusips:
            cusip = cusip.replace(" ", "")
            cleaned_cusips.append(cusip)

        item['cusip'] = "; ".join(cleaned_cusips)

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