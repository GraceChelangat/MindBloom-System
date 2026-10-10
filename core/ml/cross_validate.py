from pathlib import Path

import numpy as np
import pyreadr

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# 1. Load dataset
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "EMAnwsub.Rdata"

df = pyreadr.read_r(str(DATA_PATH))["EMAnw.sub"]

# 2. Select features and target
FEATURES = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
]

TARGET = "FC"

df = df.dropna(subset=[TARGET, "ID"]).copy()

X = df[FEATURES]
y = df[TARGET]
groups = df["ID"]

# 3. Define models
models = {
    "Baseline": DummyRegressor(strategy="mean"),

    "Ridge Regression": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("regressor", Ridge(alpha=10.0)),
    ]),

    "Random Forest": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1,
        )),
    ]),
}

# 4. Participant-grouped cross-validation
cv = GroupKFold(n_splits=5)

print("\nMINDBLOOM GROUPED CROSS-VALIDATION")
print("=" * 50)

print("Observations:", len(df))
print("Participants:", groups.nunique())

for name, model in models.items():

    scores = cross_validate(
        model,
        X,
        y,
        groups=groups,
        cv=cv,
        scoring={
            "MAE": "neg_mean_absolute_error",
            "RMSE": "neg_root_mean_squared_error",
            "R2": "r2",
        },
        n_jobs=1,
    )

    mae = -scores["test_MAE"]
    rmse = -scores["test_RMSE"]
    r2 = scores["test_R2"]

    print(f"\n{name.upper()}")
    print("-" * 40)

    print(f"Average MAE: {np.mean(mae):.4f}")
    print(f"Average RMSE: {np.mean(rmse):.4f}")
    print(f"Average R²: {np.mean(r2):.4f}")
    print(f"RMSE standard deviation: {np.std(rmse):.4f}")

print("\nCross-validation completed successfully.")