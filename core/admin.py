
from django.contrib import admin

from .models import (
    TeenagerYoungAdult,
    NutritionLifestyleQuestionnaire,
    DailyCheckIn,
)


# Customize the admin site
admin.site.site_header = "MindBloom Administration"
admin.site.site_title = "MindBloom Admin"
admin.site.index_title = "Welcome to MindBloom Administration"


@admin.register(TeenagerYoungAdult)
class TeenagerYoungAdultAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")



@admin.register(NutritionLifestyleQuestionnaire)
class NutritionLifestyleQuestionnaireAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'age',
        'gender_identity',
        'meals_per_day',
        'submitted_at',
    )

    list_filter = (
        'gender_identity',
        'submitted_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    ordering = ('-submitted_at',)

    readonly_fields = (
        'submitted_at',
    )

    list_per_page = 20



@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "mood_level",
        "stress_level",
        "sleep_hours",
        "eating_difficulties",
        "created_at",
    )

    list_filter = (
        "mood_level",
        "stress_level",
        "eating_difficulties",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)
    list_per_page = 20

    readonly_fields = ("created_at",)
