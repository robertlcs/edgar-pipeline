import argparse

import csv
import json
import re
import sys
import os

from cleaning import clean_item
from validation import validate_item

def gen_clean_items(items):
    for item in items:
        clean_item(item)
        yield item

def gen_items_from_csv(csv_input):
    reader = csv.DictReader(csv_input)
    return [row for row in reader]

def gen_validated_items(items):
    for item in items:
        validation_result = validate_item(item)
        item['is_valid'] = validation_result['is_valid']
        item['validation_reason'] = validation_result.get('reason')

        yield item

def gen_rows_from_items_with_multiple_cusips(items):
    for item in items:
        if not item.get('cusip') or not item['is_valid']:
            yield item
            continue

        cusip_numbers = item['cusip'].split(';')
        issue_names = [''] * len(cusip_numbers)

        print "Cusip numbers: " + str(cusip_numbers)
        # Fill in issue_names with values from the list of issue names
        if item['issue_name']:
            tokens = item['issue_name'].split(';')
            print "Issue names: " + str(tokens)

            for i, token in enumerate(tokens):
                if i > len(issue_names) - 1:
                    break
                issue_names[i] = token

        for i, cusip_number in enumerate(cusip_numbers):
            new_item = item.copy()
            new_item['cusip'] = cusip_number.strip()
            new_item['issue_name'] = issue_names[i].strip()
            yield new_item

def score_item_relevance(item):
    score = 0
    from cleaning import strip_issuer_name

    if item.get('issuer_name'):
        if item['issuer_name'].lower() == item['filing_person'].lower():
            score += 100
        elif strip_issuer_name(item['issuer_name']).lower() == strip_issuer_name(item['filing_person']).lower():
            score += 50

        if item['issuer_name'].lower == item['search_term'].lower():
            score += 100
        elif strip_issuer_name(item['issuer_name']).lower() == strip_issuer_name(item['search_term']).lower():
            score += 50
        return score

    if item['search_term'].lower() == item['filing_person'].lower():
        score += 70
    elif strip_issuer_name(item['search_term']).lower() == strip_issuer_name(item['filing_person']).lower():
        score += 50
    return score

def score_item_address(item):
    return (1 if item.get('address') else 0) * (len(item.get('address')) if item.get('address') else 0)

def gen_scored_items(items):
    for item in items:
        if not item['is_valid']:
            item['score'] = 0
            yield item
            continue

        item['score'] = score_item_address(item) + score_item_relevance(item) + len(item['issue_name'])

        yield item

def filing_key(item):
    return ':'.join([item['cusip'],
                     item['issuer_name'] if item.get('issuer_name') else '',
                     item['filing_person'],
                     item['issue_name']])

def process_generated_items(items):
    print "Processing items..."
    duplicate_items = []
    rejected_items = []

    # Keep track of filings we've seen before
    filings = dict()
    item_count = 0
    for item in items:
        item_count += 1
        #print item
        if not item['is_valid']:
            rejected_items.append(item)
            continue
        seen_item = filings.get(filing_key(item))

        if not seen_item:
            filings[filing_key(item)] = item
        elif item['score'] > seen_item['score']:
            filings[filing_key(item)] = item
            duplicate_items.append(seen_item)
        else:
            duplicate_items.append(item)

    print "Processed %d items." % item_count
    validated_items = filings.values()
    print "%d duplicate items" % len(duplicate_items)
    print "%d rejected items" % len(rejected_items)
    print "%d validated items" % len(validated_items)

    return {'duplicate_items' : duplicate_items,
            'rejected_items' : rejected_items,
            'validated_items' : validated_items}

parser = argparse.ArgumentParser(description='Process crawled items.')
parser.add_argument("path", help="Path to crawl output")
args = parser.parse_args()
batch_name = os.path.splitext(args.path)[0]

try:
    print "Removing processed-data..."
    os.unlink("processed-data")
except:
    print "No processed-data. It must be your first time running this script."

# Steps: Clean, validate, expand rows, score, de-dupe

print "Opening " + args.path
f = open(args.path, "r")

# Load items, using appropriate method for format (json-lines or csv)
if re.match(".*\.jl$", args.path):
    items = (json.loads(line) for line in f)
elif re.match(".*\.csv$", args.path):
    items = gen_items_from_csv(f)
    print "%d items " % len(items)
else:
    print "Input file must be in csv (.csv) or json lines (.jl) format."
    sys.exit(-1)

cleaned_items = gen_clean_items(items)
validated_items = gen_validated_items(cleaned_items)
expanded_items = gen_rows_from_items_with_multiple_cusips(validated_items)
scored_items = gen_scored_items(expanded_items)
processed_items = process_generated_items(scored_items)

fields = ['cusip', 'url', 'address', 'search_term', 'issue_name', 'filing_person', 'issuer_name', 'document_name', 'document_type', 'date']

# Create processed directory for staging processed files
dirname = batch_name + "-processed"
if not os.path.exists(dirname):
    os.mkdir(dirname)

# Write out rejects:
print "Writing rejected items..."
with open(os.path.join(dirname, "rejected-items.csv"), "w") as rejected_items_csv:
    rejected_items_writer = csv.DictWriter(rejected_items_csv, fields + ['is_valid', 'validation_reason'])
    rejected_items_writer.writeheader()
    for item in processed_items['rejected_items']:
        del item['score'] # Score is meaningless for invalid records
        rejected_items_writer.writerow(item)

# Write out duplicates:
print "Writing duplicate items..."
with open(os.path.join(dirname, "duplicate-items.csv"), "w") as duplicate_items_csv:
    duplicate_items_writer = csv.DictWriter(duplicate_items_csv, fields + ['score'])
    duplicate_items_writer.writeheader()
    for item in processed_items['duplicate_items']:
        del item['is_valid']
        del item['validation_reason']
        duplicate_items_writer.writerow(item)

# Write out valid items:
print "Writing valid items..."
with open(os.path.join(dirname, "valid-items.csv"), "w") as valid_items_csv:
    valid_items_writer = csv.DictWriter(valid_items_csv, fields + ['score'])
    valid_items_writer.writeheader()
    for item in processed_items['validated_items']:
        del item['is_valid']
        del item['validation_reason']
        valid_items_writer.writerow(item)

print "Output is in processed-data -> %s" % dirname
os.symlink(dirname, "processed-data")



