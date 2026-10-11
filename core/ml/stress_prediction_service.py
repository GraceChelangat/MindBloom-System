
"""
MindBloom Exploratory Stress Prediction Service

Purpose:
    Load the saved Ridge Regression pipeline and
    generate exploratory stress-related predictions.

Important:
    This is NOT a clinical relapse-risk predictor.
"""

import json
from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# STEP 1: DEFINE MODEL FILE LOCATIONS
# --------------------------------------------------

# Locate the folder containing this Python file.
ML_DIRECTORY = Path(__file__).resolve().parent

# Define the directory containing saved models.
MODEL_DIRECTORY = ML_DIRECTORY / "models"

# Saved Ridge Regression pipeline.
MODEL_PATH = (
    MODEL_DIRECTORY / "mindbloom_stress_ridge.joblib"
)

# Metadata describing the model's expected inputs.
METADATA_PATH = (
    MODEL_DIRECTORY
    / "mindbloom_stress_ridge_metadata.json"
)


# --------------------------------------------------
# STEP 2: LOAD THE SAVED MODEL
# --------------------------------------------------

def load_stress_model():
    """
    Load the trained pipeline and its metadata.

    Returns:
        tuple: (trained_model, metadata)

    Raises:
        FileNotFoundError:
            If the saved model or metadata is missing.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    # Only load trusted model artifacts created
    # within the MindBloom project.
    model = joblib.load(MODEL_PATH)

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    return model, metadata


# --------------------------------------------------
# STEP 3: GENERATE AN EXPLORATORY PREDICTION
# --------------------------------------------------


def predict_stress(feature_values):
    """
    Generate an exploratory stress-related prediction.

    Parameters:
        feature_values (dict):
            Six emotional measurements recorded on
            a presumed 0–100 scale.

    Returns:
        float: Predicted stress-related score.

    Important:
        This is not a clinical relapse-risk prediction.
        The input scale must be verified against the
        original dataset documentation.
    """

    # STEP 1: Check the input format.
    if not isinstance(feature_values, dict):
        raise TypeError(
            "Feature values must be provided as a dictionary."
        )

    # STEP 2: Load the trained pipeline and metadata.
    model, metadata = load_stress_model()

    required_features = metadata["features"]

    # STEP 3: Check for missing predictors.
    missing_features = [
        feature for feature in required_features
        if feature not in feature_values
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # STEP 4: Check for unexpected predictors.
    unexpected_features = [
        feature for feature in feature_values
        if feature not in required_features
    ]

    if unexpected_features:
        raise ValueError(
            f"Unexpected features: {unexpected_features}"
        )

    # STEP 5: Validate numerical values.
    validated_values = {}

    for feature in required_features:

        value = feature_values[feature]

        # Reject booleans, text and missing values.
        if isinstance(value, bool):
            raise ValueError(
                f"{feature} must be a numerical value."
            )

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"{feature} must be a numerical value."
            )

        # Reject NaN and infinite values.
        import math

        if not math.isfinite(numeric_value):
            raise ValueError(
                f"{feature} must be a finite number."
            )

        # Provisional validation based on observed
        # dataset values. Confirm the instrument scale
        # before using this beyond demonstration.
        if not 0 <= numeric_value <= 100:
            raise ValueError(
                f"{feature} must be between 0 and 100."
            )

        validated_values[feature] = numeric_value

    # STEP 6: Convert inputs into a DataFrame.
    input_data = pd.DataFrame(
        [validated_values],
        columns=required_features
    )

    # STEP 7: Generate the exploratory prediction.
    prediction = model.predict(input_data)

    return float(prediction[0])
