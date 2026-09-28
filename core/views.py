from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import TeenagerYoungAdult


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already in use.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with that email already exists.')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        TeenagerYoungAdult.objects.create(
            user=user,
            name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_number=contact_number
        )

        messages.success(
            request,
            'Account created successfully. You can now log in.'
        )

        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password. Please try again.'
        )

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required(login_url='login')
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


def resources(request):
    return render(request, 'resources.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def contact(request):
    return render(request, 'contact.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')