from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.decorators import admin_required
from accounts.models import SystemLog, ActivityLog, CompanyRecruiter


@admin_required
def admin_dashboard(request):
    User = get_user_model()
    total_users = User.objects.count()
    total_logs = SystemLog.objects.count()
    total_companies = CompanyRecruiter.objects.count()

    return render(request, 'admin/dashboard.html', {
        'total_users': total_users,
        'total_logs': total_logs,
        'total_companies': total_companies,
    })


@admin_required
def manage_users(request):
    User = get_user_model()
    role = request.GET.get('role')

    if request.method == 'POST':
        if 'delete_user_id' in request.POST:
            user_id = request.POST.get('delete_user_id')
            try:
                user_to_delete = User.objects.get(id=user_id)
                if user_to_delete != request.user:
                    SystemLog.objects.create(
                        user=request.user,
                        action="Deleted user",
                        details=f"Deleted {user_to_delete.username} (role={user_to_delete.role})"
                    )
                    user_to_delete.delete()
            except User.DoesNotExist:
                messages.error(request, "User not found.")

        elif 'toggle_active_user_id' in request.POST:
            user_id = request.POST.get('toggle_active_user_id')
            try:
                user_to_toggle = User.objects.get(id=user_id)
                if user_to_toggle != request.user:
                    user_to_toggle.is_active = not user_to_toggle.is_active
                    user_to_toggle.save()

                    SystemLog.objects.create(
                        user=request.user,
                        action="Toggled user status",
                        details=f"{user_to_toggle.username} is now {'Active' if user_to_toggle.is_active else 'Inactive'}"
                    )
            except User.DoesNotExist:
                messages.error(request, "User not found.")

    users = User.objects.filter(role=role) if role else User.objects.exclude(role__isnull=True).exclude(role='')

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_users.html', {
        'page_obj': page_obj,
        'selected_role': role
    })


@admin_required
def view_system_logs(request):
    logs = SystemLog.objects.order_by('-timestamp')
    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/view_logs.html', {
        'page_obj': page_obj,
    })


@admin_required
def monitor_activity(request):
    activities = ActivityLog.objects.select_related('user').order_by('-timestamp')

    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/monitor_activity.html', {
        'page_obj': page_obj
    })
