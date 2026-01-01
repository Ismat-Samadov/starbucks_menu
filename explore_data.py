import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('starbucks.csv')

# Display basic information
print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"\nTotal records: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")

print("\n" + "="*80)
print("BEVERAGE CATEGORIES")
print("="*80)
print(df['Beverage_category'].value_counts())

print("\n" + "="*80)
print("UNIQUE BEVERAGES")
print("="*80)
print(f"Total unique beverages: {df['Beverage'].nunique()}")
print(df['Beverage'].value_counts().head(10))

print("\n" + "="*80)
print("BASIC STATISTICS")
print("="*80)
print(df.describe())

print("\n" + "="*80)
print("SAMPLE DATA")
print("="*80)
print(df.head(20))
