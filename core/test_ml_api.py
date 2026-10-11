
"""
MindBloom Exploratory ML API Tests

Tests:
1. Unauthenticated users cannot access the API.
2. Authenticated users can submit valid inputs.
3. Invalid measurements are rejected.
4. Malformed JSON is rejected.
5. GET requests are not allowed.
"""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ExploratoryStressAPITests(TestCase):

    def setUp(self):
        """
        Create a test user and synthetic
        emotional measurements.
        """

        User = get_user_model()

        self.user = User.objects.create_user(
            username="ml_test_user",
            password="TestPassword123!"
        )

        self.url = reverse(
            "exploratory_stress_prediction"
        )

        self.valid_data = {
            "E_cheerful": 60,
            "E_enthusiastic": 55,
            "E_relaxed": 70,
            "E_calm": 65,
            "E_irritated": 20,
            "E_depressed": 15
        }

    def test_login_required(self):
        """
        Unauthenticated users should be redirected
        to the login page.
        """

        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 302)

    def test_valid_prediction(self):
        """
        Authenticated users should receive a
        successful exploratory prediction.
        """

        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertIn("prediction", result)
        self.assertEqual(
            result["model"],
            "Ridge Regression"
        )
        self.assertFalse(
            result["clinical_relapse_prediction"]
        )

    def test_invalid_range(self):
        """
        Reject measurements outside the
        provisional accepted range.
        """

        self.client.force_login(self.user)

        invalid_data = self.valid_data.copy()
        invalid_data["E_cheerful"] = 150

        response = self.client.post(
            self.url,
            data=json.dumps(invalid_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        """
        Reject malformed JSON.
        """

        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            data="{invalid json}",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        """
        The endpoint should accept POST only.
        """

        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
