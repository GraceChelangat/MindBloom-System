from django import forms

from .models import NutritionLifestyleQuestionnaire as Q


class NutritionLifestyleQuestionnaireForm(forms.Form):
    # Section 1
    age = forms.IntegerField(min_value=15, max_value=24)
    gender_identity = forms.ChoiceField(
        choices=Q.GENDER_CHOICES, widget=forms.RadioSelect
    )
    current_situation = forms.MultipleChoiceField(
        choices=Q.CURRENT_SITUATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # Section 2
    meals_per_day = forms.ChoiceField(
        choices=Q.MEALS_PER_DAY_CHOICES, widget=forms.RadioSelect
    )
    breakfast_days_per_week = forms.ChoiceField(
        choices=Q.DAYS_0_1_2_3_4_5_7_CHOICES, widget=forms.RadioSelect
    )
    meals_outside_home_frequency = forms.ChoiceField(
        choices=Q.FREQUENCY_WEEKLY_CHOICES, widget=forms.RadioSelect
    )
    dietary_pattern = forms.MultipleChoiceField(
        choices=Q.DIETARY_PATTERN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    dietary_pattern_other = forms.CharField(max_length=100, required=False)

    # Section 3
    freq_fruits_vegetables = forms.ChoiceField(
        choices=Q.FOOD_GROUP_FREQUENCY_CHOICES, widget=forms.RadioSelect
    )
    freq_whole_grains = forms.ChoiceField(
        choices=Q.FOOD_GROUP_FREQUENCY_CHOICES, widget=forms.RadioSelect
    )
    freq_lean_proteins = forms.ChoiceField(
        choices=Q.FOOD_GROUP_FREQUENCY_CHOICES, widget=forms.RadioSelect
    )
    freq_dairy_or_alternatives = forms.ChoiceField(
        choices=Q.FOOD_GROUP_FREQUENCY_CHOICES, widget=forms.RadioSelect
    )
    freq_processed_snacks = forms.ChoiceField(
        choices=Q.FOOD_GROUP_FREQUENCY_CHOICES, widget=forms.RadioSelect
    )

    # Section 4
    water_cups_per_day = forms.ChoiceField(
        choices=Q.WATER_CUPS_CHOICES, widget=forms.RadioSelect
    )
    sugar_sweetened_beverage_frequency = forms.ChoiceField(
        choices=Q.SUGAR_BEVERAGE_CHOICES, widget=forms.RadioSelect
    )
    caffeinated_beverages_per_day = forms.ChoiceField(
        choices=Q.CAFFEINE_CHOICES, widget=forms.RadioSelect
    )

    # Section 5
    physical_activity_days_per_week = forms.ChoiceField(
        choices=Q.DAYS_0_1_2_3_4_5_7_CHOICES, widget=forms.RadioSelect
    )
    screen_time_hours_per_day = forms.ChoiceField(
        choices=Q.SCREEN_TIME_CHOICES, widget=forms.RadioSelect
    )
    sleep_hours_weekdays = forms.ChoiceField(
        choices=Q.SLEEP_HOURS_CHOICES, widget=forms.RadioSelect
    )

    # Section 6
    supplements = forms.MultipleChoiceField(
        choices=Q.SUPPLEMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    supplements_other = forms.CharField(max_length=100, required=False)
    physical_symptoms = forms.MultipleChoiceField(
        choices=Q.PHYSICAL_SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # Section 7
    skipped_meals_due_to_cost = forms.ChoiceField(
        choices=Q.YES_NO_CHOICES, widget=forms.RadioSelect
    )
    confidence_access_healthy_meal = forms.ChoiceField(
        choices=Q.CONFIDENCE_CHOICES, widget=forms.RadioSelect
    )

    def save(self, user=None):
        data = self.cleaned_data
        return Q.objects.create(
            user=user if user and user.is_authenticated else None,
            age=data['age'],
            gender_identity=data['gender_identity'],
            current_situation=data['current_situation'],
            meals_per_day=data['meals_per_day'],
            breakfast_days_per_week=data['breakfast_days_per_week'],
            meals_outside_home_frequency=data['meals_outside_home_frequency'],
            dietary_pattern=data['dietary_pattern'],
            dietary_pattern_other=data['dietary_pattern_other'],
            freq_fruits_vegetables=data['freq_fruits_vegetables'],
            freq_whole_grains=data['freq_whole_grains'],
            freq_lean_proteins=data['freq_lean_proteins'],
            freq_dairy_or_alternatives=data['freq_dairy_or_alternatives'],
            freq_processed_snacks=data['freq_processed_snacks'],
            water_cups_per_day=data['water_cups_per_day'],
            sugar_sweetened_beverage_frequency=data['sugar_sweetened_beverage_frequency'],
            caffeinated_beverages_per_day=data['caffeinated_beverages_per_day'],
            physical_activity_days_per_week=data['physical_activity_days_per_week'],
            screen_time_hours_per_day=data['screen_time_hours_per_day'],
            sleep_hours_weekdays=data['sleep_hours_weekdays'],
            supplements=data['supplements'],
            supplements_other=data['supplements_other'],
            physical_symptoms=data['physical_symptoms'],
            skipped_meals_due_to_cost=data['skipped_meals_due_to_cost'],
            confidence_access_healthy_meal=data['confidence_access_healthy_meal'],
        )
