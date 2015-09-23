# edgar-pipeline
Pipeline for processing scraped Edgar documents

# Dependencies:
cusiputils

# Instructions:
python process.py path

# Example:
python process items.jl

Note: Input must be a file in which each line is a JSON object.

## Processing Amazon Mechanical Turk batches:

Some additional processing was required to map the batch results to files that can be processed as crawl items. This
processing is found in process-amt-batch.py and the output is written to the intermediate file amt_batch_results.csv.

Because the AMT jobs were missing the "Date" column, this script imports the data into sqlite and joins with the rejected_items table, then
writes the results to amt_batch_results.csv.
It can only be executed successfully if the rejected_items from the initial job were ingested first.

The commands:

python process-crawled-items.py ca6b4be65c7711e5a6c502312cb755f7.jl
python process-amt-batch.py Batch_2093436_batch_results.csv Batch_2093566_batch_results.csv
python process-crawled-items.py -i amt_batch_items.csv
