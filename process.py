import csv
import json
import sys

from cleaning import clean_item
from validation import validate_item

def usage():
    print "Usage: python process.py <path-to-file>"

def gen_clean_items(items):
    for item in items:
        clean_item(item)
        yield item

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
        issue_names = item['issue_name'].split(';')
        for i, cusip_number in enumerate(cusip_numbers):
            new_item = item.copy()
            new_item['cusip'] = cusip_number.strip()
            new_item['issue_name'] = issue_names[i].strip()
            yield new_item

def gen_scored_items(items):
    for item in items:
        if not item['is_valid']:
            item['score'] = 0
            yield item
            continue

        item['score'] = (1 if item.get('address') else 0) * (len(item.get('address')) if item.get('address') else 0 + len(item['issue_name']))
        yield item

# It would be really nice to rewrite this as a generator or series of generators, but it would require further thought.
# Or, another approach would be to load the generated items into a database and use the database to filter out
# the rejected, duplicate and valid items.
# For now, just iterate over the items and separate into categories (validated, duplicate, rejected).
def process_generated_items(items):
    duplicate_items = []
    rejected_items = []

    # Keep track of cusip's we've seen before
    cusip_to_items = dict()
    for item in items:
        print item
        if not item['is_valid']:
            rejected_items.append(item)
            continue
        seen_item = cusip_to_items.get(item['cusip'])

        if not seen_item:
            cusip_to_items[item['cusip']] = item
        elif item['score'] > seen_item['score']:
            cusip_to_items[item['cusip']] = item
            duplicate_items.append(seen_item)

    validated_items = cusip_to_items.values()
    return {'duplicate_items' : duplicate_items,
            'rejected_items' : rejected_items,
            'validated_items' : validated_items}

if len(sys.argv) < 2:
    usage()
    sys.exit(-1)

path = sys.argv[1]

# Steps: Clean, validate, expand rows, score, de-dupe

f = open(path, "r")
items = (json.loads(line) for line in f)
cleaned_items = gen_clean_items(items)
validated_items = gen_validated_items(cleaned_items)
expanded_items = gen_rows_from_items_with_multiple_cusips(validated_items)
scored_items = gen_scored_items(expanded_items)
processed_items = process_generated_items(scored_items)

fields = ['cusip', 'url', 'address', 'issue_name', 'issuer_name', 'document_name', 'date']

# Write out rejects:
with open("rejected-items.csv", "w") as rejected_items_csv:
    rejected_items_writer = csv.DictWriter(rejected_items_csv, fields + ['is_valid', 'validation_reason'])
    rejected_items_writer.writeheader()
    for item in processed_items['rejected_items']:
        del item['score'] # Score is meaningless for invalid records
        rejected_items_writer.writerow(item)

# Write out duplicates:
with open("duplicate-items.csv", "w") as duplicate_items_csv:
    duplicate_items_writer = csv.DictWriter(duplicate_items_csv, fields + ['score'])
    duplicate_items_writer.writeheader()
    for item in processed_items['duplicate_items']:
        del item['is_valid']
        del item['validation_reason']
        duplicate_items_writer.writerow(item)

# Write out valid items:
with open("valid-items.csv", "w") as valid_items_csv:
    valid_items_writer = csv.DictWriter(valid_items_csv, fields)
    valid_items_writer.writeheader()
    for item in processed_items['validated_items']:
        del item['is_valid']
        del item['validation_reason']
        del item['score']
        valid_items_writer.writerow(item)






