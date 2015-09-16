import re
import sys

def usage():
    print "Usage: python clean-input-companies.py"

def clean(line, index):
    if index == 0:
        return line.strip()

    m = re.match(r'"(.*)"', line)
    if m:
        line = m.group(1)

    cleaned_line = line.upper().strip()
    if re.search(r'CORPORATION', line, re.IGNORECASE):
        cleaned_line = cleaned_line.replace('CORPORATION', 'CORP')

    m = re.match(r'(.*) CLASS [A-Z]$', cleaned_line)
    if m:
        cleaned_line = m.group(1)

    m = re.match(r'(.*)&*\s*COMPANY$', cleaned_line)
    if m and m.group(1):
        cleaned_line = m.group(1)

    m = re.match(r'(.*) INCORPORATED$', cleaned_line)
    if m:
        cleaned_line = m.group(1) + " INC"

    m = re.match(r'(.*) & CO\.(.*)$', cleaned_line)
    if m:
        cleaned_line = m.group(1) + m.group(2)

    cleaned_line = cleaned_line.replace('-', ' ')
    cleaned_line = cleaned_line.replace('&', ' AND ')
    cleaned_line = cleaned_line.replace('.', ' ')

    cleaned_line = re.sub('\s+', ' ', cleaned_line).strip()
    return "\"%s\"" % cleaned_line

index = 0
for line in sys.stdin:
    print clean(line, index)
    index += 1

