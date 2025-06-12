# ✅ adminpanel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('view-logs/', views.view_system_logs, name='view_system_logs'),
    path('monitor-activity/', views.monitor_activity, name='monitor_activity'),
]