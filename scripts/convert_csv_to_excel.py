from pathlib import Path
import pandas as pd

# Use the full absolute path
processed_folder = Path(r"C:\Users\larry\Projects\basys_project\data\processed\20260330_110956")

claims_df = pd.read_csv(processed_folder / "merged_cleaned_claims.csv")
summary_df = pd.read_csv(processed_folder / "merged_member_summary.csv")

claims_df.to_excel(processed_folder / "merged_cleaned_claims.xlsx", index=False)
summary_df.to_excel(processed_folder / "merged_member_summary.xlsx", index=False)

print("Excel files created in:", processed_folder)
