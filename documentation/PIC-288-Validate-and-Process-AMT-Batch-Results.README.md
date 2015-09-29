Summary of steps for Amazon Mechanical Turk Processing

This is a record of the steps that were performed to ingest the Scrapy crawl items, generate HIT's and process/ingest
the batch results. Also, at the end is a summary of the statistics that were generated before the AMT batch results
and after.

The HIT's were created from the rejected items of the first crawl. The idea of doing the HIT's was that these items could be
extracted manually, if not by machine, and would improve the coverage of our target data set for S&P 500 companies.

The first step was to process the crawled items and ingest them into Sqlite:

  python process-crawled-items.py ca6b4be65c7711e5a6c502312cb755f7.jl
  python ingest.py ca6b4be65c7711e5a6c502312cb755f7-processed/

Next, we looked for all the Schedule 13G's and Schedule 13G/A's in the rejected_items table:

    .output missing-cusips-13G.csv
    select * from rejected_items where document_name like '%13G%';

We could have narrowed this group down further by eliminating documents that appear in both valid_items
and rejected_items. We cannot be certain that the documents don't contain unique information, but if we already have
 parsed a document with the same title, there's a good chance that rejected document contains nothing new.

  select count(*) from rejected_items where document_name
like '%13G%' and document_name not in (select document_name from valid_items),

This yielded the missing-cusips-13G.csv file. This file contained 343 rows (one was a header):

  (myenv)USAU9900:edgar-pipeline reedn$ wc -l missing-cusips-13G.csv
  343 missing-cusips-13G.csv

This was split into two smaller files to be submitted separately as HIT's:

  (myenv)USAU9900:edgar-pipeline reedn$ wc -l missing-cusips-13G-HIT.csv
        20 missing-cusips-13G-HIT.csv
  (myenv)USAU9900:edgar-pipeline reedn$ wc -l missing-cusips-13G-HIT2.csv
       324 missing-cusips-13G-HIT2.csv

Once the HIT's were available, some creative munging was required to get all the fields.  The "Date" field was missing
because it wasn't submitted as part of the job. Although this isn't critical, I did some work to restore that field.
Also, the files had to be mapped to the CSV format that is expected in the "process-crawl-results.py" script.

The "process_amt_batch.py" script loads the data from the batch files, joins them with the rejected items using the
query below, and writes the output to new CSV file, "amt_batch_items.csv".

SQL for Joining amt_batch_items with rejected_items:

    select a.cusip, a.url, a.address, a.issuer_name, a.issue_name, a.document_name, b.date
    from amt_batch_items as a, rejected_items as b where a.url = b.url;"

Script:

  python process_amt_batch.py Batch_2093436_batch_results.csv Batch_2093566_batch_results-utf-8.csv

Some of the AMT results were converted to UTF-8, as the there were some encoding errors encountered when attempting to process
the CSV file. This method might not be correct, as a few of the CUSIP's were garbled and appear to contain special characters
that are represented with numeric sequences.

The output from this script is a CSV file that has the fields cusip, url, document_name, issue_name, issuer_name, and date. This
can now be processed using the same script we used to process the crawler output:

    python process-crawled-items.py amt_batch_items.csv

Next, we generated metrics to get a baseline, then ingested the processed amt_batch_items (using -i for incremental ingest, which
does not create or drop any tables):

(myenv)USAU9900:edgar-pipeline reedn$ python generate_metrics.py
----- Crawl results -----
# items crawled: 10117
# items valid: 2879
# items rejected: 6480
# items duplicates: 758
Percentage accepted (valid): 0.28

------------ Stocks and Bonds ------------
Number of common stocks: 977
Number of issues (CUSIP's): 2879

---------- S&P 500 Index -----------
# of common stocks for SP500: 346
# of companies in index: 502
Percentage of S&P 500 common stocks found/accepted: 0.69
(myenv)USAU9900:edgar-pipeline reedn$ python ingest.py -i amt_batch_items-processed/
(myenv)USAU9900:edgar-pipeline reedn$ python generate_metrics.py
----- Crawl results -----
# items crawled: 11151
# items valid: 2981
# items rejected: 6654
# items duplicates: 1516
Percentage accepted (valid): 0.27

------------ Stocks and Bonds ------------
Number of common stocks: 1066
Number of issues (CUSIP's): 2905

---------- S&P 500 Index -----------
# of common stocks for SP500: 384
# of companies in index: 502
Percentage of S&P 500 common stocks found/accepted: 0.76

ANALYSIS OF RESULTS

To get an idea of the gross number of issues from the AMT batch, we can count the number of lines in the valid,
rejected and duplicate items files:

(myenv)USAU9900:edgar-pipeline reedn$ wc -l amt_batch_items-processed/valid-items.csv
     103 amt_batch_items-processed/valid-items.csv
(myenv)USAU9900:edgar-pipeline reedn$ wc -l amt_batch_items-processed/rejected-items.csv
     175 amt_batch_items-processed/rejected-items.csv
(myenv)USAU9900:edgar-pipeline reedn$ wc -l amt_batch_items-processed/duplicate-items.csv
     759 amt_batch_items-processed/duplicate-items.csv

We added 103 new valid items from the batch. How many of these were unique vs. duplicates? We have to query the database to get that.

It turns out quite a few of these were duplicates of valid items. A script was written to remove duplicate "valid" items:

(myenv)USAU9900:edgar-pipeline reedn$ python dedupe-db.py
...
G60754101
N90064101
76 cusips found with duplicate rows
76 rows deleted

After removing the duplicates, I regenerated the metrics:

(myenv)USAU9900:edgar-pipeline reedn$ python generate_metrics.py
----- Crawl results -----
# items crawled: 11075
# items valid: 2905
# items rejected: 6654
# items duplicates: 1516
Percentage accepted (valid): 0.26

------------ Stocks and Bonds ------------
Number of common stocks: 1000
Number of issues (CUSIP's): 2905

---------- S&P 500 Index -----------
# of common stocks for SP500: 349
# of companies in index: 502
Percentage of S&P 500 common stocks found/accepted: 0.70

The number of valid items is not much higher. Only 3 additional S&P 500 common stocks were
found.

The rejected and duplicate counts below are probably inflated by the duplicates and rejected items from the AMT
batch, which reduced the percentage "accepted (valid)".

The total count of stocks went from 977 (after the first crawl was ingested) to 1000, and the number of issues went from
2879 to 2905.

We targeted 344 documents for submission to Amazon Mechanical Turk:

(myenv)USAU9900:edgar-pipeline reedn$ wc -l missing-cusips-13G-HIT.csv
      20 missing-cusips-13G-HIT.csv
(myenv)USAU9900:edgar-pipeline reedn$ wc -l missing-cusips-13G-HIT2.csv
     324 missing-cusips-13G-HIT2.csv

The batch file was 1026 lines, with approximately 3 entries per document. As expected, this is about the same number of
documents that were submitted in HIT's (342).

The AMT job increased the issue count by 26 and the number of common stocks by 3. The percentage went from 69% to 70%.
Going through the rejected items, I found a few common errors, many of which originated in the source documents (invalid
CUSIP checksums, invalid length).

It appears that most of the rejected documents were rejected because they contained invalid data or were missing
critical information like CUSIP #'s.

Conclusions / Learnings:

- The AMT job was not very targeted. There were similar filings that were filed on multiple dates for the same company, so
they appeared to be distinct documents but contained the same CUSIP #'s. The crux of the problem is that we can't know
without actually seeing the documents if they contain unique information so the search has to be as inclusive as
possible.

- When the HIT's were generated, I didn't cross-check the rejected documents with valid and duplicate items. It might have
been possible to reduce the size of the HIT's by excluding items that were duplicated in those tables, although it would
be difficult to determine in the case of missing CUSIP #'s (since that is the only relevant unique identifier, not the document
titles or url's).

- Some of the information is just missing from the source documents. Also, it appears that some of the companies do not have
 public filings on sec.gov that contain CUSIP's for their common stocks.

- If we relax the standards for CUSIP's, then both the rejected items and the HIT job size would be smaller, but the tradeoff
is potentially bad data.

- There is potential for manual error. I explicitly instructed workers to separate multiple values using semicolons (;'s),
since some values like issue names can contain comma's (eg. Common Stock, par value $0.01 per share). Despite the
instructions, commas were used in a few cases.  In the future, HIT's should probably just use multiple answer fields when there are
potentially multiple values. Of course, there is still the possibility of missing data.
