import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "..", "food-bank", "live1.csv")
df = pd.read_csv(csv_path)

output_tex = os.path.join(script_dir, "tables.tex")
tex_file = open(output_tex, "w")

def show_and_save(df_table, title, float_format=None, index=False):
    print(f"=== {title} ===")
    print(df_table.to_markdown(index=index))
    print()
    tex_file.write(f"% {title}\n")
    tex_file.write(df_table.to_latex(index=index, float_format=float_format))
    tex_file.write("\n")

# --- 1a: Første rader ---
show_and_save(df.head(), "First 5 rows", float_format="%.0f")

# --- 1a: Summary statistics ---
summary = df.describe().round(2)
show_and_save(summary, "Summary statistics", float_format="%.2f", index=True)

# --- 1a: Datatyper ---
dtypes_df = df.dtypes.reset_index()
dtypes_df.columns = ["Column", "Dtype"]
show_and_save(dtypes_df, "Data types")

# --- 1b: Manglende verdier ---
missing = df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing count"]
missing["Missing %"] = (missing["Missing count"] / len(df) * 100).round(2)
show_and_save(missing, "Missing values", float_format="%.2f")

# --- 1b: Unike verdier ---
categorical_cols = ["Area", "Item", "Element", "Unit"]
unique_summary = pd.DataFrame({
    "Column": categorical_cols,
    "Unique count": [df[c].nunique() for c in categorical_cols]
})
show_and_save(unique_summary, "Unique values per categorical column")

# --- 1b: Outliers (IQR-metode) ---
Q1 = df["Value"].quantile(0.25)
Q3 = df["Value"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df["Value"] < lower) | (df["Value"] > upper)]

outlier_summary = pd.DataFrame({
    "Metric": ["Q1", "Q3", "IQR", "Lower bound", "Upper bound", "Outlier count", "Outlier %"],
    "Value": [Q1, Q3, IQR, lower, upper, len(outliers), round(len(outliers)/len(df)*100, 2)]
})
show_and_save(outlier_summary, "Outlier summary (IQR method)", float_format="%.2f")

tex_file.close()
print(f"LaTeX-tabeller lagret i: {output_tex}")