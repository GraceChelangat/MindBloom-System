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

print("\n" + "=" * 50)
print("MINDBLOOM ML SUITABILITY CHECK")
print("=" * 50)

df = datasets["EMAnw.sub"]

print("\n1. UNIQUE PARTICIPANTS:")
print(df["ID"].nunique())

print("\n2. PARTICIPANT GROUPS:")
print(df.groupby("Group", observed=True)["ID"].nunique())

print("\n3. AGE DISTRIBUTION (PARTICIPANT LEVEL):")
participants = df.drop_duplicates(subset="ID")
print(participants["Age"].describe())

print("\n4. FOOD CRAVING TARGET (FC):")
print(df["FC"].describe())

print("\n5. MISSING VALUES IN CANDIDATE FEATURES:")
features = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
    "FC",
]

print(df[features].isnull().sum())

print("\n6. COMPLETE RECORDS FOR PROTOTYPE:")
print(df[features].dropna().shape[0])