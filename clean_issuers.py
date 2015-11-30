import csv

# Take the issuer-cusip6's and standardize issuer names
from cleaning import strip_issuer_name

with open("issuer-cusip6s.csv", "r") as issuers_csv:
    reader = csv.DictReader(issuers_csv)
    with open("cleaned-issuer-cusip6s.csv", "w") as issuers_out_csv:
        writer = csv.DictWriter(issuers_out_csv, fieldnames = ['CUSIP6', 'SEARCH_TERM', 'ISSUER_NAME', 'ADDRESS'])
        writer.writeheader()


        with open("cleaned-issuer-cusip6s-rejected.csv", "w") as rejected_out_csv:
            rejected_writer = csv.DictWriter(rejected_out_csv, fieldnames=['CUSIP6', 'SEARCH_TERM', 'ISSUER_NAME', 'CLEANED_SEARCH_TERM', 'CLEANED_ISSUER_NAME'])
            for row in reader:
                cleaned_search_term = strip_issuer_name(row['SEARCH_TERM'])
                cleaned_issuer_name = strip_issuer_name(row['ISSUER_NAME'])

                if cleaned_issuer_name == cleaned_search_term:
                    row = {'SEARCH_TERM' : row['SEARCH_TERM'],
                           'ISSUER_NAME' : row['ISSUER_NAME'],
                           'CUSIP6' : row['CUSIP6'],
                           'ADDRESS' : row['ADDRESS']}
                    writer.writerow(row)
                else:
                    print "Rejecting %s, %s" % (cleaned_issuer_name, cleaned_search_term)
                    rejected_writer.writerow({'CUSIP6' : row['CUSIP6'],
                                              'CLEANED_SEARCH_TERM' : cleaned_search_term,
                                              'CLEANED_ISSUER_NAME' : cleaned_issuer_name,
                                              'SEARCH_TERM' : row['SEARCH_TERM'],
                                              'ISSUER_NAME' : row['ISSUER_NAME']})
