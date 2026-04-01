# basys_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# --- Paths
# -----------------------------
project_root = Path(__file__).resolve().parent.parent
processed_root = project_root / "data" / "processed"
temp_folder = project_root / "temp"
temp_folder.mkdir(exist_ok=True)

# -----------------------------
# --- Load latest cleaned CSV
# -----------------------------
# pick the latest merged_cleaned_claims*.csv from any subfolder
csv_files = sorted(processed_root.glob("*/merged_cleaned_claims*.csv"))  # include subfolders
if not csv_files:
    raise FileNotFoundError("No merged_cleaned_claims CSV found in processed folder or its subfolders.")

latest_csv = csv_files[-1]
df = pd.read_csv(latest_csv, parse_dates=["date_of_service"])
print(f"Loaded {latest_csv}, {len(df)} rows")

# -----------------------------
# --- Add helper columns
# -----------------------------
df["year"] = df["date_of_service"].dt.year
df["month"] = df["date_of_service"].dt.month
df["high_cost"] = df["claim_amt"] > 10000

# -----------------------------
# --- 1. Total claims per member
# -----------------------------
claims_per_member = df.groupby("member_name")["claim_amt"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
claims_per_member.plot(kind="bar", color="skyblue")
plt.ylabel("Total Claims ($)")
plt.title("Total Claims per Member")
plt.tight_layout()
plt.savefig(temp_folder / "total_claims_per_member.png")
plt.close()

# -----------------------------
# --- 2. High-cost claims per member
# -----------------------------
high_cost_counts = df[df["high_cost"]].groupby("member_name").size().sort_values(ascending=False)
plt.figure(figsize=(8,5))
high_cost_counts.plot(kind="bar", color="salmon")
plt.ylabel("High-Cost Claims (#)")
plt.title("High-Cost Claims per Member")
plt.tight_layout()
plt.savefig(temp_folder / "high_cost_claims_by_member.png")
plt.close()

# -----------------------------
# --- 3. Duplicate claims
# -----------------------------
duplicates = df.groupby(["member_name","date_of_service","claim_amt"]).size().reset_index(name="count")
duplicates = duplicates[duplicates["count"] > 1]
if not duplicates.empty:
    plt.figure(figsize=(8,5))
    duplicates.plot(kind="bar", x="member_name", y="count", color="orange")
    plt.title("Duplicate Claims per Member")
    plt.tight_layout()
    plt.savefig(temp_folder / "duplicate_claims.png")
    plt.close()

# -----------------------------
# --- 4. Members with multiple claims in same month
# -----------------------------
multi_claims = df.groupby(["member_name","year","month"]).size().reset_index(name="num_claims")
multi_claims = multi_claims[multi_claims["num_claims"] > 1]
if not multi_claims.empty:
    plt.figure(figsize=(10,5))
    for name, group in multi_claims.groupby("member_name"):
        plt.plot(group["month"], group["num_claims"], marker='o', label=name)
    plt.xlabel("Month")
    plt.ylabel("Number of Claims")
    plt.title("Members with Multiple Claims in Same Month")
    plt.legend()
    plt.tight_layout()
    plt.savefig(temp_folder / "multiple_claims_same_month.png")
    plt.close()

# -----------------------------
# --- 5. Members whose total claims exceed $10,000
# -----------------------------
total_claims = df.groupby("member_name")["claim_amt"].sum()
over_10k = total_claims[total_claims > 10000].sort_values(ascending=False)
plt.figure(figsize=(8,5))
over_10k.plot(kind="bar", color="purple")
plt.ylabel("Total Claims ($)")
plt.title("Members with Total Claims > $10,000")
plt.tight_layout()
plt.savefig(temp_folder / "claims_over_10k.png")
plt.close()

# -----------------------------
# --- 6. Average claim amount per member
# -----------------------------
avg_claim = df.groupby("member_name")["claim_amt"].mean().sort_values(ascending=False)
plt.figure(figsize=(8,5))
avg_claim.plot(kind="bar", color="green")
plt.ylabel("Average Claim ($)")
plt.title("Average Claim Amount per Member")
plt.tight_layout()
plt.savefig(temp_folder / "avg_claim_per_member.png")
plt.close()

# -----------------------------
# --- 7. Top 20 claims by amount
# -----------------------------
top20_claims = df.sort_values("claim_amt", ascending=False).head(20)
plt.figure(figsize=(8,5))
plt.barh(top20_claims["member_name"], top20_claims["claim_amt"], color="teal")
plt.xlabel("Claim Amount ($)")
plt.title("Top 20 Claims by Amount")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(temp_folder / "top20_claims.png")
plt.close()

# -----------------------------
# --- 8. Monthly total claims
# -----------------------------
monthly_totals = df.groupby(["year","month"])["claim_amt"].sum()
plt.figure(figsize=(8,5))
monthly_totals.plot(kind="line", marker="o")
plt.ylabel("Total Claims ($)")
plt.title("Monthly Total Claims")
plt.tight_layout()
plt.savefig(temp_folder / "monthly_total_claims.png")
plt.close()

print(f"Charts saved in {temp_folder}")

# -----------------------------
# --- 9. High-cost claims in a specific month (March 2026 as example)
# -----------------------------
specific_month = df[(df["high_cost"]) & (df["year"] == 2026) & (df["month"] == 3)]
if not specific_month.empty:
    plt.figure(figsize=(8,5))
    plt.bar(specific_month["member_name"], specific_month["claim_amt"], color="red")
    plt.ylabel("Claim Amount ($)")
    plt.title("High-Cost Claims in March 2026")
    plt.tight_layout()
    plt.savefig(temp_folder / "high_cost_claims_mar2026.png")
    plt.close()

# -----------------------------
# --- 10. Count of claims per month
# -----------------------------
claims_per_month = df.groupby(["year","month"]).size()
plt.figure(figsize=(8,5))
claims_per_month.plot(kind="line", marker="o", color="blue")
plt.ylabel("Number of Claims")
plt.title("Number of Claims per Month")
plt.tight_layout()
plt.savefig(temp_folder / "claims_count_per_month.png")
plt.close()

# -----------------------------
# --- 11. Average claim amount per month
# -----------------------------
avg_claim_per_month = df.groupby(["year","month"])["claim_amt"].mean()
plt.figure(figsize=(8,5))
avg_claim_per_month.plot(kind="line", marker="o", color="orange")
plt.ylabel("Average Claim ($)")
plt.title("Average Claim Amount per Month")
plt.tight_layout()
plt.savefig(temp_folder / "avg_claim_per_month.png")
plt.close()
