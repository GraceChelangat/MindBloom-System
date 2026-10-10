from pathlib import Path

import numpy as np
import pyreadr

from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# =====================================================
# 1. LOAD DATASET
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "EMAnwsub.Rdata"

df = pyreadr.read_r(str(DATA_PATH))["EMAnw.sub"]

df = df.dropna(subset=["FC", "ID"]).copy()

TARGET = "FC"
y = df[TARGET]
groups = df["ID"]


# =====================================================
# 2. DEFINE FEATURE SETS
# =====================================================

original_features = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
]

expanded_features = original_features + [
    "E_irritated",
    "E_dissatisfied",
    "E_bored",
    "E_cheerful",
    "E_relaxed",
    "E_calm",
    "E_enthusiastic",
]

feature_sets = {
    "Original Features": original_features,
    "Expanded Emotional Features": expanded_features,
}


# =====================================================
# 3. DEFINE MODELS
# =====================================================

baseline = DummyRegressor(strategy="mean")

ridge_model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("regressor", Ridge(alpha=10.0)),
])

cv = GroupKFold(n_splits=5)


# =====================================================
# 4. RUN EXPERIMENTS
# =====================================================

print("\nMINDBLOOM FEATURE EXPERIMENTS")
print("=" * 55)

print("Observations:", len(df))
print("Participants:", groups.nunique())

# Baseline does not depend on feature selection
baseline_scores = cross_validate(
    baseline,
    df[original_features],
    y,
    groups=groups,
    cv=cv,
    scoring={
        "MAE": "neg_mean_absolute_error",
        "RMSE": "neg_root_mean_squared_error",
        "R2": "r2",
    },
)

print("\nBASELINE")
print("-" * 45)
print(f"Average MAE: {-np.mean(baseline_scores['test_MAE']):.4f}")
print(f"Average RMSE: {-np.mean(baseline_scores['test_RMSE']):.4f}")
print(f"Average R²: {np.mean(baseline_scores['test_R2']):.4f}")


for name, features in feature_sets.items():

    X = df[features]

    scores = cross_validate(
        ridge_model,
        X,
        y,
        groups=groups,
        cv=cv,
        scoring={
            "MAE": "neg_mean_absolute_error",
            "RMSE": "neg_root_mean_squared_error",
            "R2": "r2",
        },
    )

    print(f"\n{name.upper()}")
    print("-" * 45)

    print("Number of features:", len(features))
    print(f"Average MAE: {-np.mean(scores['test_MAE']):.4f}")
    print(f"Average RMSE: {-np.mean(scores['test_RMSE']):.4f}")
    print(f"Average R²: {np.mean(scores['test_R2']):.4f}")


print("\nFeature experiments completed successfully.")