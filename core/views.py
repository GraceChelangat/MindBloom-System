from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import NutritionLifestyleQuestionnaireForm


def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def login_view(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def nutrition_questionnaire(request):
    if request.method == 'POST':
        form = NutritionLifestyleQuestionnaireForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Your questionnaire has been saved. Thank you!')
            return redirect('dashboard')
    else:
        form = NutritionLifestyleQuestionnaireForm()

    return render(request, 'nutrition_questionnaire.html', {'form': form})