
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator

from .models import TeenagerYoungAdult, DailyCheckIn
from .forms import DailyCheckInForm, NutritionLifestyleQuestionnaireForm


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
    messages.success(
        request,
        'You have been logged out successfully.'
    )
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    checkins = DailyCheckIn.objects.filter(
        user=request.user
    ).order_by('-created_at')

    latest_checkin = checkins.first()
    today = timezone.localdate()

    checked_in_today = checkins.filter(
        created_at__date=today
    ).exists()

    recent_checkins = list(checkins[:7])
    recent_checkins.reverse()

    chart_points = []

    for checkin in recent_checkins:
        chart_points.append({
            'date': timezone.localtime(
                checkin.created_at
            ).strftime('%d %b'),
            'mood': checkin.mood_level,
            'stress': checkin.stress_level,
        })

    context = {
        'latest_checkin': latest_checkin,
        'checked_in_today': checked_in_today,
        'total_checkins': checkins.count(),
        'recent_checkins': recent_checkins,
        'chart_points': chart_points,
    }

    return render(request, 'dashboard.html', context)




@login_required(login_url='login')
def checkin_history(request):
    checkins = DailyCheckIn.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Read optional date filters from the URL
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    # Validate the dates before filtering
    from django.utils.dateparse import parse_date

    valid_from_date = parse_date(from_date) if from_date else None
    valid_to_date = parse_date(to_date) if to_date else None

    if valid_from_date:
        checkins = checkins.filter(
            created_at__date__gte=valid_from_date
        )

    if valid_to_date:
        checkins = checkins.filter(
            created_at__date__lte=valid_to_date
        )

    # Count matching check-ins
    total_checkins = checkins.count()

    # Display 6 records per page
    paginator = Paginator(checkins, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'checkins': page_obj,
        'page_obj': page_obj,
        'total_checkins': total_checkins,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(
        request,
        'checkin_history.html',
        context
    )


@login_required(login_url='login')
def nutrition_questionnaire(request):
    if request.method == 'POST':
        form = NutritionLifestyleQuestionnaireForm(request.POST)

        if form.is_valid():
            form.save(user=request.user)
            messages.success(
                request,
                'Your questionnaire has been saved. Thank you!'
            )
            return redirect('dashboard')
    else:
        form = NutritionLifestyleQuestionnaireForm()

    return render(
        request,
        'nutrition_questionnaire.html',
        {'form': form}
    )


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


@login_required(login_url='login')
def daily_checkin(request):
    if request.method == 'POST':
        form = DailyCheckInForm(request.POST)

        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.user = request.user
            checkin.save()

            messages.success(
                request,
                'Your daily check-in has been saved successfully!'
            )
            return redirect('dashboard')
    else:
        form = DailyCheckInForm()

    return render(
        request,
        'checkin.html',
        {'form': form}
    )
