# ✅ accounts/views.py (Final Refactored Version)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from accounts.models import Student, CompanyRecruiter, PlacementCoordinator, SystemLog
from accounts.decorators import student_required, recruiter_required, coordinator_required, admin_required
from django.views.decorators.cache import never_cache

# Role-to-dashboard mapping
ROLE_DASHBOARD_MAP = {
    'student': 'student_dashboard',
    'recruiter': 'company_dashboard',
    'coordinator': 'coordinator_dashboard',
    'admin': 'admin_dashboard',
}

def home(request):
    return render(request, 'landing.html')

def home_redirect(request):
    return redirect('login')

@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect(ROLE_DASHBOARD_MAP.get(request.user.role, 'home'))

    if request.method == 'POST':
        role = request.POST.get('role', 'student')
        form = RegistrationForm(request.POST, role=role)
        if form.is_valid():
            user = form.save()

            if role == 'student':
                Student.objects.create(user=user)
            elif role == 'recruiter':
                company_name = request.POST.get('company_name', '')
                CompanyRecruiter.objects.create(user=user, company_name=company_name)
            elif role == 'coordinator':
                PlacementCoordinator.objects.create(user=user)
            elif role == 'admin':
                user.is_staff = True
                user.save()

            SystemLog.objects.create(
                user=user,
                action="User Registered",
                details=f"Registered as {user.role}"
            )
            login(request, user)
            return redirect(ROLE_DASHBOARD_MAP.get(role, 'home'))
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect(ROLE_DASHBOARD_MAP.get(request.user.role, 'home'))

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            SystemLog.objects.create(
                user=user,
                action="User Logged In",
                details=f"Role: {user.role}"
            )
            return redirect(ROLE_DASHBOARD_MAP.get(user.role, 'home'))
        else:
            error = "Invalid username or password"
    return render(request, 'accounts/login.html', {'error': error})


@never_cache
def logout_view(request):
    if request.user.is_authenticated:
        SystemLog.objects.create(
            user=request.user,
            action="User Logged Out",
            details=""
        )
    logout(request)
    return redirect('login')
