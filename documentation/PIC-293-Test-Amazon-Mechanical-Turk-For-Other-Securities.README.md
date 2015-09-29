# Amazon Mechanical Turk and Notes / Other Securities (not Common Stocks)

For this POC, we have a larger potential search space, and it would be good to narrow it down to a smaller one for 
cost reasons.

## Narrowing down the search space

Potential documents:

    sqlite> select count(*) from rejected_items where document_name not like '%13G%';
    6138

How many of these have unique titles?

    sqlite> select count(distinct document_name) from rejected_items where document_name not like '%13G%';
    2829

Next we look at the unique document titles (these may or may not be unique if they were filed on different dates, contain
different information, etc.). Below we build up a query to find the distinct document titles for companies, first
those outside the S&P 500, then those in the S&P 500, which we then select into a new table and then we count this second group:

    select distinct document_name from rejected_items
    where document_name not like '%13G%' and issuer_name not in (select company from sp500_companies)
    group by issuer_name;
    ...
    
    select distinct document_name from rejected_items
    where document_name not like '%13G%' and issuer_name in (select company from sp500_companies)
    group by issuer_name;
    ...
    
    create table distinct_document_names as select distinct document_name from rejected_items
    where document_name not like '%13G%' and issuer_name in (select company from sp500_companies)
    group by issuer_name;

    select count(*) from distinct_document_names;
    301


Only a portion of these don't appear in valid_items:

    select count(*) from distinct_document_names where document_name not in (select document_name from valid_items);
    278

We will use this set of document titles to submit a small set of HIT's to find the securities contained within.

    sqlite> .mode csv
    sqlite> .output distinct_documents_not_13g_HIT.csv
    sqlite> select url, issuer_name, d.document_name, date from rejected_items as r, distinct_document_names as d where r.document_name = d.document_name;