import pandas as pd
from pathlib import Path

# Paths
project_root = Path(__file__).parent.parent
csv_path = project_root / 'data/cleaned/cleaned_emi_prediction_dataset.csv'
parquet_path = project_root / 'data/cleaned/cleaned_emi_prediction_dataset.parquet'

def convert():
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Saving to {parquet_path}...")
    df.to_parquet(parquet_path, engine='pyarrow', index=False)
    
    print("✅ Conversion successful!")
    print(f"CSV Size: {csv_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"Parquet Size: {parquet_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    convert()
