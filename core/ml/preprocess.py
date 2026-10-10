from pathlib import Path
import pyreadr
from sklearn.model_selection import GroupShuffleSplit
from sklearn.impute import SimpleImputer

# Dataset location
DATA_PATH = Path(__file__).parent / "data" / "EMAnwsub.Rdata"

# Load dataset
datasets = pyreadr.read_r(str(DATA_PATH))
df = datasets["EMAnw.sub"]

# Features related to emotional state
FEATURES = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
]

# Observed food craving is our prototype target
TARGET = "FC"

# Remove observations without a known target
df = df.dropna(subset=[TARGET]).copy()

X = df[FEATURES]
y = df[TARGET]
groups = df["ID"]

# Split by participant, not by individual observation
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42,
)

train_idx, test_idx = next(
    splitter.split(X, y, groups=groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

# Fit imputer on training data only
imputer = SimpleImputer(strategy="median")

X_train_processed = imputer.fit_transform(X_train)
X_test_processed = imputer.transform(X_test)

print("\nMINDBLOOM DATA PREPROCESSING")
print("=" * 45)

print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))

print("Training participants:", groups.iloc[train_idx].nunique())
print("Testing participants:", groups.iloc[test_idx].nunique())

print("Missing values after preprocessing:")
print("Training:", int(X_train_processed.shape[0] * X_train_processed.shape[1] -
                       __import__("numpy").isfinite(X_train_processed).sum()))
print("Testing:", int(X_test_processed.shape[0] * X_test_processed.shape[1] -
                      __import__("numpy").isfinite(X_test_processed).sum()))

print("\nPreprocessing completed successfully.")