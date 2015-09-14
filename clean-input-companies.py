import re
import sys

def usage():
    print "Usage: python clean-input-companies.py"

def clean(line):
    cleaned_line = line.upper().strip()
    if re.search(r'CORPORATION', line, re.IGNORECASE):
        cleaned_line = cleaned_line.replace('CORPORATION', 'CORP')

    m = re.match(r'(.*) CLASS [A-Z]$', cleaned_line)
    if m:
        cleaned_line = m.group(1)

    return cleaned_line

for line in sys.stdin:

    print clean(line)

