# Python CSV and Regex Tasks with System Design

This repository contains Python scripts to solve the following tasks:

1. CSV Task: Convert tsv to csv and add a price_edited column
2. Regex Task: Filter out knit products without jumpers
3. Design Task: Propose an optimized system for product catalog processing

## Requirements

- Python 3.8 or above
- Required packages listed in requirements.txt:
  - pandas==2.0.3

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Files

- `csv-task.py`: Script to convert tsv to csv and add price_edited column
- `regex-task.py`: Script to filter out knit products without jumpers using regex
- `python_home_task_file.tsv`: Original input file (tsv format)
- `requirements.txt`: List of required packages
- `design-task.md`: A plan for optimizing the current implementation of processing catalogs.

## Usage

### CSV Task

This script performs two operations:
1. Converts a tsv file to csv format and saves it as an intermediate file
2. Adds a 'price_edited' column filled with float values from the 'search_price' column

```bash
python csv-task.py --infile python_home_task_file.tsv --out python_home_task_file_with_price.csv
```

The script automatically detects whether the input file is tsv or csv format based on its content, regardless of the file extension. It produces two output files:
- An intermediate csv file (renamed from .tsv to .csv if applicable)
- The final csv file with the price_edited column added

### Regex Task

This script removes all knit products that don't contain "jumper" from the input csv file:

```bash
python regex-task.py --infile python_home_task_file.csv --out python_home_task_file_regex.csv
```

## Implementation Details

### CSV Task

- Uses pandas to read the tsv/csv file efficiently
- Automatically detects the input file format based on content analysis, not relying on file extensions
- Implements a robust delimiter detection algorithm to determine if a file is tsv or csv format
- Converts 'search_price' column to float and handles missing/invalid values
- Adds 'price_edited' column with numeric values
- Handles quoting and special characters properly when writing the output csv file

### Regex Task

- Uses pandas for data manipulation and regex for pattern matching
- Creates separate text fields for knit detection and jumper detection
- Looks for "knit" or "knitwear" in all relevant columns including description
- Looks for "jumper" only in product name and category fields, NOT in descriptions
- Uses word boundary markers in regex to ensure accurate matching
- Uses non-capturing regex groups to avoid pandas warnings
- Distinguishes between "jumper" and "jumpsuit" using negative lookahead assertions
- Filters out rows that match 'knit' but don't match 'jumper' (case insensitive)
- Preserves all other rows in the output file
- Reports the number of rows removed during filtering

## Error Handling

Both scripts include error handling for:
- File not found
- Permission errors
- Missing columns
- Invalid data types

## Design Task Solution

The repository also includes a solution to the design task in the file `design-task.md`. 

This document presents a progressive implementation plan for optimizing product catalog processing with AI image tagging. The solution addresses the inefficiencies in the current system by:

1. Implementing change detection to avoid unnecessary processing
2. Differentiating between types of changes (metadata vs. image)
3. Using optimized indexing strategies for Elasticsearch
4. Introducing a streaming architecture for efficient processing
5. Adding advanced monitoring and optimization

The implementation plan is structured in levels, allowing for incremental improvements with clear benefits at each stage.
