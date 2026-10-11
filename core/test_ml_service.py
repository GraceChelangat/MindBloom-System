
"""
Automated tests for MindBloom's exploratory
machine-learning prediction service.
"""

from django.test import SimpleTestCase

from core.ml.stress_prediction_service import (
    load_stress_model,
    predict_stress
)


class StressPredictionServiceTests(SimpleTestCase):

    def setUp(self):
        """
        Prepare synthetic example measurements
        before each test.
        """
        self.valid_data = {
            "E_cheerful": 60,
            "E_enthusiastic": 55,
            "E_relaxed": 70,
            "E_calm": 65,
            "E_irritated": 20,
            "E_depressed": 15
        }

    def test_model_loads_successfully(self):
        """
        Confirm that the saved pipeline and
        metadata can be loaded.
        """
        model, metadata = load_stress_model()

        self.assertIsNotNone(model)
        self.assertEqual(
            metadata["target"],
            "E_nervous_stressed"
        )

    def test_valid_prediction(self):
        """
        Confirm that valid input generates
        a numerical prediction.
        """
        prediction = predict_stress(self.valid_data)

        self.assertIsInstance(prediction, float)

    def test_invalid_range_rejected(self):
        """
        Reject measurements outside the
        provisional accepted range.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["E_cheerful"] = 150

        with self.assertRaises(ValueError):
            predict_stress(invalid_data)

    def test_missing_feature_rejected(self):
        """
        Reject inputs missing a required feature.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["E_calm"]

        with self.assertRaises(ValueError):
            predict_stress(invalid_data)

    def test_text_input_rejected(self):
        """
        Reject non-numerical measurements.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["E_relaxed"] = "very relaxed"

        with self.assertRaises(ValueError):
            predict_stress(invalid_data)

    def test_unexpected_feature_rejected(self):
        """
        Reject additional, unrecognized predictors.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["unknown_feature"] = 50

        with self.assertRaises(ValueError):
            predict_stress(invalid_data)
