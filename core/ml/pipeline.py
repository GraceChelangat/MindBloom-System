"""
MindBloom Machine Learning Pipeline

This module will contain the preprocessing, training and prediction
pipeline used by MindBloom to estimate relapse-risk patterns.

IMPORTANT:
The model is intended as a research/prototype risk-monitoring tool.
It is not a clinical diagnosis system.
"""


# ---------------------------------------------------------
# Feature groups
# ---------------------------------------------------------

MOOD_FEATURES = [
    "mood_intensity",
]

CHECKIN_FEATURES = [
    "stress_level",
    "sleep_hours",
]

EATING_BEHAVIOUR_FEATURES = [
    "meals_per_day",
    "breakfast_days_per_week",
]

LIFESTYLE_FEATURES = [
    "physical_activity_days_per_week",
    "sleep_hours_weekdays",
]

DEMOGRAPHIC_FEATURES = [
    "age",
]


# Combined model inputs
MODEL_FEATURES = (
    MOOD_FEATURES
    + CHECKIN_FEATURES
    + EATING_BEHAVIOUR_FEATURES
    + LIFESTYLE_FEATURES
    + DEMOGRAPHIC_FEATURES
)


def get_model_features():
    """
    Return the features currently planned for the
    MindBloom relapse-risk prediction pipeline.
    """
    return MODEL_FEATURES


if __name__ == "__main__":
    print("MindBloom ML Pipeline")
    print("---------------------")

    print("\nModel features:")

    for feature in get_model_features():
        print(f"- {feature}")

    print("\nTarget variable:")
    print("- To be determined from the selected research dataset")