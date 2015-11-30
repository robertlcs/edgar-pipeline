from cleaning import strip_issuer_name
import csv

# Compare distinct_issuers with sp500_companies
# select name from distinct_issuers
# select company from sp500_companies

distinct_issuers = []
sp500_companies = []

with open("distinct-issuers.csv", "r") as in_csv:
    reader = csv.DictReader(in_csv)
    for row in reader:
        distinct_issuers.append(row['issuer_name'])

with open("sp500_companies_cleaned.csv", "r") as in_csv:
    reader = csv.DictReader(in_csv)
    for row in reader:
        sp500_companies.append(row['company'])

#strip_issuer_name(company)

