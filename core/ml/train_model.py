from pathlib import Path
import joblib
import numpy as np
import pyreadr

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "EMAnwsub.Rdata"
MODEL_PATH = BASE_DIR / "models" / "food_craving_model.joblib"

FEATURES = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
]

TARGET = "FC"

# Load the research dataset
df = pyreadr.read_r(str(DATA_PATH))["EMAnw.sub"]

# Keep records with a known target and participant ID
df = df.dropna(subset=[TARGET, "ID"]).copy()

X = df[FEATURES]
y = df[TARGET]
groups = df["ID"]

# Keep participants separate between training and testing
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42,
)

train_idx, test_idx = next(splitter.split(X, y, groups=groups))

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]
y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

# Build preprocessing and model together
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )),
])

# Train the model
model.fit(X_train, y_train)

# Evaluate on unseen participants
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nMINDBLOOM MODEL TRAINING")
print("=" * 45)

print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))
print("Training participants:", groups.iloc[train_idx].nunique())
print("Testing participants:", groups.iloc[test_idx].nunique())

print("\nMODEL PERFORMANCE")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R-squared (R²): {r2:.4f}")

# Save the trained model locally
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")
print("Training completed successfully.")