from django.db import models
from django.contrib.auth.models import User


class TeenagerYoungAdult(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teenager_profile'
    )

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class NutritionLifestyleQuestionnaire(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary_other', 'Non-binary / Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    CURRENT_SITUATION_CHOICES = [
        ('student', 'Student (High School / College / University)'),
        ('employed', 'Employed (Full-time / Part-time)'),
        ('living_with_parents', 'Living with parents/guardians'),
        ('living_independently', 'Living independently / with roommates'),
    ]

    MEALS_PER_DAY_CHOICES = [
        ('1_or_fewer', '1 meal or fewer'),
        ('2', '2 meals'),
        ('3', '3 meals'),
        ('4_plus', '4+ meals'),
    ]

    DAYS_0_1_2_3_4_5_7_CHOICES = [
        ('0', '0 days'),
        ('1_2', '1–2 days'),
        ('3_4', '3–4 days'),
        ('5_7', '5–7 days'),
    ]

    FREQUENCY_WEEKLY_CHOICES = [
        ('rarely_never', 'Rarely or never'),
        ('1_2', '1–2 times per week'),
        ('3_4', '3–4 times per week'),
        ('5_plus', '5 or more times per week'),
    ]

    DIETARY_PATTERN_CHOICES = [
        ('none', 'No specific diet / Eat everything'),
        ('vegetarian_vegan', 'Vegetarian / Vegan'),
        ('halal_kosher', 'Halal / Kosher'),
        ('lactose_free', 'Lactose-free or Dairy-free'),
        ('gluten_free', 'Gluten-free'),
        ('other', 'Other'),
    ]

    FOOD_GROUP_FREQUENCY_CHOICES = [
        ('rarely_never', 'Rarely/Never'),
        ('1_2', '1–2 days/week'),
        ('3_4', '3–4 days/week'),
        ('5_7', '5–7 days/week'),
    ]

    WATER_CUPS_CHOICES = [
        ('less_than_3', 'Less than 3 cups'),
        ('3_5', '3–5 cups'),
        ('6_8', '6–8 cups'),
        ('more_than_8', 'More than 8 cups'),
    ]

    SUGAR_BEVERAGE_CHOICES = [
        ('rarely_never', 'Rarely or never'),
        ('1_3_week', '1–3 times per week'),
        ('4_6_week', '4–6 times per week'),
        ('1_plus_day', '1 or more times per day'),
    ]

    CAFFEINE_CHOICES = [
        ('0', '0'),
        ('1_2', '1–2'),
        ('3_4', '3–4'),
        ('5_plus', '5 or more'),
    ]

    SCREEN_TIME_CHOICES = [
        ('less_than_2', 'Less than 2 hours'),
        ('2_4', '2–4 hours'),
        ('5_7', '5–7 hours'),
        ('8_plus', '8 or more hours'),
    ]

    SLEEP_HOURS_CHOICES = [
        ('less_than_6', 'Less than 6 hours'),
        ('6_7', '6–7 hours'),
        ('8_9', '8–9 hours'),
        ('10_plus', '10 or more hours'),
    ]

    SUPPLEMENT_CHOICES = [
        ('none', 'None'),
        ('multivitamin', 'Multivitamin'),
        ('protein_powder', 'Protein powder / Weight gainer'),
        ('iron', 'Iron'),
        ('vitamin_d_calcium', 'Vitamin D or Calcium'),
        ('other', 'Other'),
    ]

    PHYSICAL_SYMPTOM_CHOICES = [
        ('fatigue', 'Unusual or chronic fatigue / Low energy'),
        ('dizziness', 'Frequent dizziness or lightheadedness'),
        ('digestive_issues', 'Digestive issues (bloating, severe cramping, frequent constipation/diarrhea)'),
        ('brittle_nails_hair_thinning', 'Brittle nails or unexplained hair thinning'),
        ('none', 'None of the above'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    CONFIDENCE_CHOICES = [
        ('highly_confident', 'Highly confident'),
        ('moderately_confident', 'Moderately confident'),
        ('not_confident', 'Not confident (lack of resources, time, or cooking skills)'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='nutrition_questionnaires',
        null=True,
        blank=True,
    )

    # Section 1: Demographic & General Profile
    age = models.PositiveIntegerField()
    gender_identity = models.CharField(max_length=30, choices=GENDER_CHOICES)
    current_situation = models.JSONField(default=list, blank=True)

    # Section 2: Dietary Habits & Meal Patterns
    meals_per_day = models.CharField(max_length=20, choices=MEALS_PER_DAY_CHOICES)
    breakfast_days_per_week = models.CharField(max_length=10, choices=DAYS_0_1_2_3_4_5_7_CHOICES)
    meals_outside_home_frequency = models.CharField(max_length=20, choices=FREQUENCY_WEEKLY_CHOICES)
    dietary_pattern = models.JSONField(default=list, blank=True)
    dietary_pattern_other = models.CharField(max_length=100, blank=True)

    # Section 3: Food Group Frequency
    freq_fruits_vegetables = models.CharField(max_length=20, choices=FOOD_GROUP_FREQUENCY_CHOICES)
    freq_whole_grains = models.CharField(max_length=20, choices=FOOD_GROUP_FREQUENCY_CHOICES)
    freq_lean_proteins = models.CharField(max_length=20, choices=FOOD_GROUP_FREQUENCY_CHOICES)
    freq_dairy_or_alternatives = models.CharField(max_length=20, choices=FOOD_GROUP_FREQUENCY_CHOICES)
    freq_processed_snacks = models.CharField(max_length=20, choices=FOOD_GROUP_FREQUENCY_CHOICES)

    # Section 4: Hydration & Beverage Intake
    water_cups_per_day = models.CharField(max_length=20, choices=WATER_CUPS_CHOICES)
    sugar_sweetened_beverage_frequency = models.CharField(max_length=20, choices=SUGAR_BEVERAGE_CHOICES)
    caffeinated_beverages_per_day = models.CharField(max_length=10, choices=CAFFEINE_CHOICES)

    # Section 5: Physical Activity & Lifestyle
    physical_activity_days_per_week = models.CharField(max_length=10, choices=DAYS_0_1_2_3_4_5_7_CHOICES)
    screen_time_hours_per_day = models.CharField(max_length=20, choices=SCREEN_TIME_CHOICES)
    sleep_hours_weekdays = models.CharField(max_length=20, choices=SLEEP_HOURS_CHOICES)

    # Section 6: Physical Symptoms & Supplementation
    supplements = models.JSONField(default=list, blank=True)
    supplements_other = models.CharField(max_length=100, blank=True)
    physical_symptoms = models.JSONField(default=list, blank=True)

    # Section 7: Food Security & Accessibility
    skipped_meals_due_to_cost = models.CharField(max_length=20, choices=YES_NO_CHOICES)
    confidence_access_healthy_meal = models.CharField(max_length=30, choices=CONFIDENCE_CHOICES)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        who = self.user.username if self.user else 'Anonymous'
        return f'Nutrition & Lifestyle Questionnaire — {who} ({self.submitted_at:%Y-%m-%d})'