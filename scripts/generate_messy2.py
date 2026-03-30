import pandas as pd

# New messy data
data2 = {
    "ID ": [104, 105, 106, 102, None],
    "Member Name": ["Alice Green", "Tom Brown", "Eve White", "Jane Smith", "Missing Name"],
    "Claim Amt": ["$5000", "2,300.00", "$12,500", "900", "$700"],
    "Date of Service": ["4/1/26", "2026-04-05", "04/15/2026", "02/12/2026", "4/20/26"]
}

df2 = pd.DataFrame(data2)

# Messy top rows
messy_top2 = pd.DataFrame({
    "ID ": ["Report Generated: 4/1/2026", "Client: ABC Company", "", ""],
    "Member Name": ["", "", "", ""],
    "Claim Amt": ["", "", "", ""],
    "Date of Service": ["", "", "", ""]
})

final_df2 = pd.concat([messy_top2, df2], ignore_index=True)

final_df2.to_excel("messy_basys_2.xlsx", index=False)

print("✅ Second messy file created: messy_basys_2.xlsx")