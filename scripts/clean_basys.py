import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import argparse

# -----------------------------
# --- CLI Arguments
# -----------------------------
parser = argparse.ArgumentParser(description="Clean and merge Basys Excel files")
parser.add_argument(
    "--log",
    choices=["terminal", "file", "both"],
    default="both",
    help="Logging output: terminal, file, or both (default)"
)
args = parser.parse_args()

# -----------------------------
# --- Paths
# -----------------------------
data_folder = Path("data")
raw_folder = data_folder / "raw"
processed_folder = data_folder / "processed"
logs_folder = data_folder / "logs"

# Timestamp for this run
run_time = datetime.now().strftime("%Y%m%d_%H%M%S")
processed_run_folder = processed_folder / run_time
logs_run_folder = logs_folder / run_time

# Create folders if missing
processed_run_folder.mkdir(parents=True, exist_ok=True)
logs_run_folder.mkdir(parents=True, exist_ok=True)

# -----------------------------
# --- Logging Setup
# -----------------------------
log_file_path = logs_run_folder / "run.log"

log_handlers = []
if args.log in ["terminal", "both"]:
    log_handlers.append(logging.StreamHandler())
if args.log in ["file", "both"]:
    log_handlers.append(logging.FileHandler(log_file_path, mode="w"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=log_handlers
)

logger = logging.getLogger("BasysCleaner")

# -----------------------------
# --- Functions
# -----------------------------
def clean_file(filename):
    logger.info(f"Processing file: {filename.name}")
    
    # Load without header
    df_raw = pd.read_excel(filename, header=None)
    # Find header row
    try:
        header_row_index = df_raw[df_raw.iloc[:,0].astype(str).str.strip().str.upper() == "ID"].index[0]
    except IndexError:
        logger.error(f"Header row with 'ID' not found in {filename}")
        raise
    df = pd.read_excel(filename, header=header_row_index)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    logger.info(f"Columns detected: {df.columns.tolist()}")

    # Keep track of original row count
    original_rows = len(df)

    # Drop non-numeric IDs
    df = df[pd.to_numeric(df["id"], errors="coerce").notna()]
    df["id"] = df["id"].astype(int)

    # Clean currency
    df["claim_amt"] = df["claim_amt"].replace('[\$,]', '', regex=True).astype(float)

    # Fix dates
    df["date_of_service"] = pd.to_datetime(df["date_of_service"], errors="coerce")

    # Remove duplicates
    df = df.drop_duplicates()

    # Standardize names
    df["member_name"] = df["member_name"].str.title()

    cleaned_rows = len(df)
    logger.info(f"Original rows: {original_rows}, cleaned rows: {cleaned_rows}")

    return df

# -----------------------------
# --- Main Execution
# -----------------------------
# Get all raw Excel files
raw_files = sorted(raw_folder.glob("*.xlsx"))
if not raw_files:
    raise FileNotFoundError(f"No Excel files found in {raw_folder}")

# Clean all files and keep per-file summary
dfs = []
file_summaries = []
for f in raw_files:
    df = clean_file(f)
    dfs.append(df)
    file_summaries.append((f.name, len(df)))

# Merge all cleaned data
merged_df = pd.concat(dfs, ignore_index=True)

# Actuarial logic
merged_df["year"] = merged_df["date_of_service"].dt.year
merged_df["month"] = merged_df["date_of_service"].dt.month
merged_df["high_cost"] = merged_df["claim_amt"] > 10000

# Member-level aggregation
member_summary = merged_df.groupby("id").agg(
    member_name=("member_name", "first"),
    total_claims=("claim_amt", "sum"),
    high_cost_claims=("high_cost", "sum")
).reset_index()

# Save CSV outputs
merged_csv = processed_run_folder / "merged_cleaned_claims.csv"
summary_csv = processed_run_folder / "merged_member_summary.csv"

merged_df.to_csv(merged_csv, index=False)
member_summary.to_csv(summary_csv, index=False)

# -----------------------------
# --- Logging summaries
# -----------------------------
logger.info("✅ Merged data saved:")
logger.info(f" - {merged_csv}")
logger.info(f" - {summary_csv}")

logger.info("\n--- Per-file row counts ---")
for fname, rows in file_summaries:
    logger.info(f"{fname}: {rows} cleaned rows")

logger.info(f"\nTotal merged rows: {len(merged_df)}")
logger.info("\nMember summary preview:\n%s", member_summary)
