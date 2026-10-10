from pathlib import Path

import joblib
import numpy as np
import pyreadr

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# =====================================================
# 1. FILE PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "EMAnwsub.Rdata"

MODEL_PATH = BASE_DIR / "models" / "food_craving_model.joblib"


# =====================================================
# 2. FEATURE SELECTION
# =====================================================

# Emotional and psychological features
FEATURES = [
    "PA",
    "NA",
    "E_depressed",
    "E_worried",
    "E_nervous_stressed",
    "E_tense",
]

# Target: observed food craving
TARGET = "FC"


# =====================================================
# 3. LOAD DATASET
# =====================================================

print("\nMINDBLOOM MACHINE LEARNING SYSTEM")
print("=" * 50)

print("\nLoading research dataset...")

datasets = pyreadr.read_r(str(DATA_PATH))

df = datasets["EMAnw.sub"]

print("Dataset loaded successfully.")
print("Original dataset shape:", df.shape)


# =====================================================
# 4. DATA PREPROCESSING
# =====================================================

print("\nPREPROCESSING DATA")
print("=" * 50)

# Remove records without a target or participant ID
df = df.dropna(subset=[TARGET, "ID"]).copy()

# Select model inputs
X = df[FEATURES]

# Select prediction target
y = df[TARGET]

# Participant identifiers
groups = df["ID"]

print("Available observations:", len(df))
print("Unique participants:", groups.nunique())

print("\nMissing feature values:")
print(X.isnull().sum())


# =====================================================
# 5. PARTICIPANT-LEVEL TRAIN/TEST SPLIT
# =====================================================

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

train_groups = groups.iloc[train_idx]
test_groups = groups.iloc[test_idx]

# Verify that no participant appears in both sets
assert set(train_groups).isdisjoint(set(test_groups))

print("\nDATA SPLIT SUMMARY")
print("=" * 50)

print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))

print("Training participants:", train_groups.nunique())
print("Testing participants:", test_groups.nunique())


# =====================================================
# 6. DEFINE MODELS
# =====================================================

# Model 1: Baseline
baseline_model = DummyRegressor(
    strategy="mean"
)

# Model 2: Random Forest
random_forest_model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    ),
])

# Model 3: Ridge Regression
ridge_model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "scaler",
        StandardScaler()
    ),
    (
        "regressor",
        Ridge(alpha=10.0)
    ),
])


# =====================================================
# 7. TRAIN AND EVALUATE MODELS
# =====================================================

models = {
    "Baseline": baseline_model,
    "Random Forest": random_forest_model,
    "Ridge Regression": ridge_model,
}

results = {}

print("\nMODEL TRAINING AND EVALUATION")
print("=" * 50)

for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

    # Train model
    model.fit(X_train, y_train)

    # Predict on unseen participants
    predictions = model.predict(X_test)

    # Calculate evaluation metrics
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    # Store results
    results[model_name] = {
        "model": model,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }

    print(f"\n{model_name.upper()} PERFORMANCE")
    print("-" * 40)

    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²: {r2:.4f}")


# =====================================================
# 8. MODEL COMPARISON
# =====================================================

print("\nMODEL COMPARISON")
print("=" * 65)

print(
    f"{'Model':<20}"
    f"{'MAE':<12}"
    f"{'RMSE':<12}"
    f"{'R²':<12}"
)

print("-" * 65)

for model_name, result in results.items():

    print(
        f"{model_name:<20}"
        f"{result['MAE']:<12.4f}"
        f"{result['RMSE']:<12.4f}"
        f"{result['R2']:<12.4f}"
    )


# =====================================================
# 9. SELECT BEST MODEL
# =====================================================

# Choose the model with the lowest test RMSE
best_model_name = min(
    results,
    key=lambda name: results[name]["RMSE"]
)

best_result = results[best_model_name]

print("\nBEST MODEL")
print("=" * 50)

print("Model:", best_model_name)
print(f"MAE: {best_result['MAE']:.4f}")
print(f"RMSE: {best_result['RMSE']:.4f}")
print(f"R²: {best_result['R2']:.4f}")


# =====================================================
# 10. SAVE MODEL
# =====================================================

# Only save an ML model if it outperforms the baseline
baseline_rmse = results["Baseline"]["RMSE"]

if (
    best_model_name != "Baseline"
    and best_result["RMSE"] < baseline_rmse
):

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        {
            "model": best_result["model"],
            "features": FEATURES,
            "target": TARGET,
            "model_name": best_model_name,
        },
        MODEL_PATH
    )

    print("\nMODEL SAVED SUCCESSFULLY")
    print("Location:", MODEL_PATH)

else:

    print("\nNo ML model outperformed the baseline.")
    print("No new model will be saved.")

    # Remove any previously saved model so that an
    # outdated model is not accidentally used.
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
        print("Previous model artifact removed.")


# =====================================================
# 11. FINAL SUMMARY
# =====================================================

print("\nMINDBLOOM TRAINING SUMMARY")
print("=" * 50)

print("Dataset:", "EMAnw.sub")
print("Prediction target:", TARGET)

print("Total observations:", len(df))
print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))

print("Training participants:", train_groups.nunique())
print("Testing participants:", test_groups.nunique())

print("\nTraining and evaluation completed successfully.")