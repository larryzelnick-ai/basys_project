import pandas as pd
from pathlib import Path

# Path to your latest timestamped folder
processed_folder = Path("C:/Users/larry/Projects/basys_project/data/processed/20260330_110956")

# Load the CSV
claims_df = pd.read_csv(processed_folder / "merged_cleaned_claims.csv")

# Convert high_cost to integer (0/1)
claims_df['high_cost'] = claims_df['high_cost'].map({True: 1, False: 0})

# Ensure date_of_service is in proper datetime format
claims_df['date_of_service'] = pd.to_datetime(claims_df['date_of_service'])

# Optional: reorder columns if needed
claims_df = claims_df[['id', 'member_name', 'claim_amt', 'date_of_service', 'year', 'month', 'high_cost']]

# Save to a new CSV for MySQL import
claims_df.to_csv(processed_folder / "merged_cleaned_claims_mysql.csv", index=False, encoding='utf-8')

print("Prepared CSV for MySQL import saved as merged_cleaned_claims_mysql.csv")
