
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'daily-checkin/',
        views.daily_checkin,
        name='daily_checkin'
    ),

    path(
        'checkin-history/',
        views.checkin_history,
        name='checkin_history'
    ),

    path(
        'nutrition-questionnaire/',
        views.nutrition_questionnaire,
        name='nutrition_questionnaire'
    ),

    path('resources/', views.resources, name='resources'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),
    path(
    "api/exploratory-stress/",
    views.exploratory_stress_prediction,
    name="exploratory_stress_prediction"
),
]
