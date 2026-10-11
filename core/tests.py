
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import DailyCheckIn, NutritionLifestyleQuestionnaire

from .models import DailyCheckIn


class DailyCheckInPrivacyTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="TestPassword123!"
        )

        self.user2 = User.objects.create_user(
            username="testuser2",
            password="TestPassword123!"
        )

        DailyCheckIn.objects.create(
            user=self.user1,
            mood_level=4,
            stress_level=2,
            notes="Private note belonging to user one"
        )

        DailyCheckIn.objects.create(
            user=self.user2,
            mood_level=3,
            stress_level=3,
            notes="Private note belonging to user two"
        )

    def test_history_only_shows_logged_in_users_records(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("checkin_history")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Private note belonging to user one"
        )

        self.assertNotContains(
            response,
            "Private note belonging to user two"
        )

    def test_history_requires_login(self):
        response = self.client.get(
            reverse("checkin_history")
        )

        self.assertEqual(response.status_code, 302)



from .forms import NutritionLifestyleQuestionnaireForm


class NutritionQuestionnaireTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="questionnaire_test_user",
            password="TestPassword123!"
        )

    def test_questionnaire_is_linked_to_correct_user(self):
        form = NutritionLifestyleQuestionnaireForm(
            data={
                "age": 20,
                "gender_identity": "female",
                "current_situation": ["student"],
                "meals_per_day": "3",
                "breakfast_days_per_week": "5_7",
                "meals_outside_home_frequency": "1_2",
                "dietary_pattern": ["none"],
                "freq_fruits_vegetables": "3_4",
                "freq_whole_grains": "3_4",
                "freq_lean_proteins": "3_4",
                "freq_dairy_or_alternatives": "3_4",
                "freq_processed_snacks": "1_2",
                "water_cups_per_day": "6_8",
                "sugar_sweetened_beverage_frequency": "rarely_never",
                "caffeinated_beverages_per_day": "1_2",
                "physical_activity_days_per_week": "3_4",
                "screen_time_hours_per_day": "2_4",
                "sleep_hours_weekdays": "8_9",
                "supplements": ["none"],
                "physical_symptoms": ["none"],
                "skipped_meals_due_to_cost": "no",
                "confidence_access_healthy_meal": "highly_confident",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

        questionnaire = form.save(user=self.user)

        self.assertEqual(questionnaire.user, self.user)

        self.assertEqual(
            NutritionLifestyleQuestionnaire.objects.filter(
                user=self.user
            ).count(),
            1
        )

        self.assertEqual(questionnaire.age, 20)

        self.assertEqual(
            questionnaire.current_situation,
            ["student"]
        )


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="auth_test_user",
            email="test@example.com",
            password="TestPassword123!"
        )

    def test_registered_user_can_log_in(self):
        login_successful = self.client.login(
            username="auth_test_user",
            password="TestPassword123!"
        )

        self.assertTrue(login_successful)

    def test_invalid_password_is_rejected(self):
        login_successful = self.client.login(
            username="auth_test_user",
            password="WrongPassword123!"
        )

        self.assertFalse(login_successful)

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(response.status_code, 200)
