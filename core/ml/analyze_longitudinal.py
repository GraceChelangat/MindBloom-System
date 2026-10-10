from pathlib import Path
import pandas as pd
import pyreadr

# =====================================================
# 1. LOAD DATASET
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "EMAnwsub.Rdata"

df = pyreadr.read_r(str(DATA_PATH))["EMAnw.sub"]

print("\nMINDBLOOM LONGITUDINAL DATA ANALYSIS")
print("=" * 55)

# =====================================================
# 2. PARTICIPANT GROUPS
# =====================================================

print("\n1. PARTICIPANT GROUPS")
print("-" * 45)

participants = df.drop_duplicates(subset="ID")

print(
    participants.groupby("Group", observed=True)["ID"]
    .nunique()
)

# =====================================================
# 3. OBSERVATIONS PER PARTICIPANT
# =====================================================

print("\n2. OBSERVATIONS PER PARTICIPANT")
print("-" * 45)

observations = df.groupby("ID", observed=True).size()

print(observations.describe())

# =====================================================
# 4. AGE DISTRIBUTION
# =====================================================

print("\n3. AGE DISTRIBUTION")
print("-" * 45)

print(participants["Age"].describe())

print("\nParticipants aged 13–24:")
print(participants["Age"].between(13, 24).sum())

# =====================================================
# 5. EATING-DISORDER SYMPTOM MEASUREMENT
# =====================================================

print("\n4. EATING-DISORDER SYMPTOM VARIATION")
print("-" * 45)

symptom_variation = (
    df.groupby("ID", observed=True)["EDEQ_gesamt"]
    .nunique(dropna=True)
)

print("Participants with changing EDE-Q values:")
print((symptom_variation > 1).sum())

print("Participants with one EDE-Q value:")
print((symptom_variation == 1).sum())

# =====================================================
# 6. POSSIBLE TIME VARIABLES
# =====================================================

print("\n5. POSSIBLE TIME VARIABLES")
print("-" * 45)

time_columns = [
    col for col in df.columns
    if any(
        word in col.lower()
        for word in ["date", "time", "day", "week", "session"]
    )
]

print(time_columns if time_columns else "No explicit time variables found.")

# =====================================================
# 7. SUMMARY
# =====================================================

print("\nLONGITUDINAL SUITABILITY SUMMARY")
print("=" * 55)

print("Total observations:", len(df))
print("Unique participants:", df["ID"].nunique())

print(
    "Participants with changing EDE-Q values:",
    (symptom_variation > 1).sum()
)

print("Explicit time columns:", len(time_columns))

print("\nAnalysis completed successfully.")