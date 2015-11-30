from cusiputils.validation import validate_cusip

MULTI_VALUE_DELIMITTER = ';'

def validate_item(item, validate_issue_names=False):
    if not item.get('cusip'):
        return {'is_valid' : False, 'reason' : 'No CUSIP #'}

    cusips = item['cusip'].split(MULTI_VALUE_DELIMITTER)
    for cusip in cusips:
        result = validate_cusip(cusip)
        if not result['is_valid']:
            return result

    if validate_issue_names:
        if not item['issue_name']:
            return {'is_valid' : False, 'reason' : 'No issue name'}

        if len(item['issue_name']) > 200:
            return {'is_valid' : False, 'reason' : 'Issue name is suspiciously long'}

        issue_names = item['issue_name'].split(MULTI_VALUE_DELIMITTER)
        cusips = item['cusip'].split(MULTI_VALUE_DELIMITTER)
        if len(cusips) > len(issue_names):
            return {'is_valid' : False, 'reason' : "Insufficient issue names for given CUSIP #'s"}

    # Validate the address. This would be a good place to add a call to an address validation library, if
    # we had one. The cleaning should have taken care of most address parsing problems.
    # For now, just reject really long addresses.

    if item.get('address') and len(item['address']) > 150:
        return {'is_valid' : False, 'reason' : 'Invalid address!'}

    return {'is_valid' : True}
