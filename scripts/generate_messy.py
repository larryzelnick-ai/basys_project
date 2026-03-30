import pandas as pd

# Step 1a: Create the core data
data = {
    "ID ": [101, 102, 103, 101, None],
    "Member Name": ["John Smith", "jane smith", "Bob Lee", "John Smith", "Missing Name"],
    "Claim Amt": ["$1,200.50", "850.00", "$15,000", "$1,200.50", "$500"],
    "Date of Service": ["1/5/26", "2026-02-10", "03/15/2026", "1/5/26", "2/1/26"]
}

df = pd.DataFrame(data)

# Step 1b: Add messy rows above (simulate real Excel report)
messy_top = pd.DataFrame({
    "ID ": ["Report Generated: 3/1/2026", "Client: ABC Company", "", "", ""],
    "Member Name": ["", "", "", "", ""],
    "Claim Amt": ["", "", "", "", ""],
    "Date of Service": ["", "", "", "", ""]
})

# Combine messy top rows with actual data
final_df = pd.concat([messy_top, df], ignore_index=True)

# Step 1c: Save to Excel
final_df.to_excel("messy_basys.xlsx", index=False)

print("✅ Messy Excel file created: messy_basys.xlsx")