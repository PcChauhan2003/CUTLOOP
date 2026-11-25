import pandas as pd
df = pd.read_csv("c:/Users/dhruv/OneDrive/Desktop/ds/CUTLOOP/cutloop_ds/datasets/processed/garments_cleaned.csv.gz")
print("dominant_fiber value_counts:")
print(df["dominant_fiber"].value_counts().head(10))
print("\nFirst 5 rows of dominant_fiber and dominant_pct:")
print(df[["dominant_fiber", "dominant_pct", "cotton", "polyester", "elastane"]].head(10))
