# Basys Project Data Cleaning

This repository contains scripts to clean and merge claims data from raw Excel files and generate summary CSVs.

## Project Structure

```text
basys_project/
├── data/
│   ├── raw/               # Original Excel files (.xlsx) used as input
│   ├── processed/         # Merged output CSVs, organized in timestamped folders
│   └── logs/              # Run logs, organized in timestamped folders
├── scripts/
│   ├── clean_basys.py     # Main cleaning and merging script
│   ├── generate_messy.py  # Script to generate sample messy Excel file 1
│   └── generate_messy2.py # Script to generate sample messy Excel file 2
├── requirements.txt       # Python dependencies
└── README.md
```

## Prerequisites
- Python 3.x (or 2.7 if necessary)
- pandas
- openpyxl (for reading .xlsx)

Install dependencies via:
```bash
pip install -r requirements.txt
```

## Usage

Place your raw Excel files in data/raw/. They should contain at least the following columns:

```text
ID
Member Name
Claim Amt
Date of Service
```

Run the cleaning script:
```bash
python scripts/clean_basys.py
```

## What the script does:

1. Detects header row automatically in each Excel file.
2. Cleans data:
    - Strips whitespace and normalizes column names.
    - Converts IDs to numeric.
    - Cleans currency values.
    - Parses dates.
    - Removes duplicates.
    - Standardizes member names.
3. Merges all Excel files into a single dataset.
4. Adds actuarial logic:
    - Extracts year and month from date_of_service.
    - Flags high_cost claims (claim_amt > 10,000).
5. Generates member-level aggregation:
    - total_claims and high_cost_claims.
6. Saves output to a timestamped processed folder:

```text
data/processed/YYYYMMDD_HHMMSS/
- merged_cleaned_claims.csv
- merged_member_summary.csv
```

Each run saves the merged CSVs inside a new folder under data/processed/ with the timestamp in the folder name.

7. Logs the run in a timestamped logs folder:
```text
data/logs/YYYYMMDD_HHMMSS/run.log
```

## Quick Output Example

A small preview of `merged_member_summary.csv` after running the script:

```csv
id,member_name,total_claims,high_cost_claims
101,John Smith,1200.5,0
102,Jane Smith,1750.0,0
103,Bob Lee,15000.0,1
104,Alice Green,5000.0,0
```

## Notes
- Raw Excel files remain untouched in **data/raw/**.
- Each run produces new timestamped folders under **data/processed/**, preventing overwrites.
- Run logs are saved under **data/logs/** with matching timestamps.
- The script prints a member summary preview to the terminal.
- Raw Excel files in **data/raw/** should **not** be committed to Git. They are excluded via `.gitignore`.