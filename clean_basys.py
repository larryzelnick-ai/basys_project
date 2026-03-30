import pandas as pd

def clean_file(filename):
    # Load without header
    df_raw = pd.read_excel(filename, header=None)
    header_row_index = df_raw[df_raw.iloc[:,0].astype(str).str.strip() == "ID"].index[0]
    df = pd.read_excel(filename, header=header_row_index)
    
    # Clean columns
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    
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
    
    return df

# Clean both files
df1 = clean_file("messy_basys.xlsx")
df2 = clean_file("messy_basys_2.xlsx")

# Merge them
merged_df = pd.concat([df1, df2], ignore_index=True)

# Add actuarial logic
merged_df["year"] = merged_df["date_of_service"].dt.year
merged_df["month"] = merged_df["date_of_service"].dt.month
merged_df["high_cost"] = merged_df["claim_amt"] > 10000

# Member-level aggregation
member_summary = merged_df.groupby("id").agg(
    member_name=("member_name", "first"),
    total_claims=("claim_amt", "sum"),
    high_cost_claims=("high_cost", "sum")
).reset_index()

# Save merged results
merged_df.to_csv("merged_cleaned_claims.csv", index=False)
member_summary.to_csv("merged_member_summary.csv", index=False)

print("✅ Merged data saved:")
print(" - merged_cleaned_claims.csv")
print(" - merged_member_summary.csv")
print("\nMember summary preview:")
print(member_summary)