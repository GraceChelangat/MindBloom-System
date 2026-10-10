from pathlib import Path
import pyreadr

# Locate the dataset
DATA_PATH = Path(__file__).parent / "data" / "EMAnwsub.Rdata"

# Load the R dataset
datasets = pyreadr.read_r(str(DATA_PATH))

print("\nMINDBLOOM DATASET INSPECTION")
print("=" * 50)

for name, df in datasets.items():

    print(f"\nDataset name: {name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nCOLUMN NAMES:")
    for column in df.columns:
        print(f"- {column}")

    print("\nFIRST FIVE RECORDS:")
    print(df.head().to_string())

    print("\nMISSING VALUES:")
    print(df.isnull().sum().sort_values(ascending=False).head(20))

    print("\nDATA TYPES:")
    print(df.dtypes)

print("\nInspection completed successfully.")