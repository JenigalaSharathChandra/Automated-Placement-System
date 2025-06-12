# ✅ coordinator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('approve-jobs/', views.approve_jobs, name='approve_jobs'),
    path('approve-job/<int:job_id>/', views.approve_job_action, name='approve_job_action'),
    path('monitor-applications/', views.monitor_applications, name='monitor_applications'),
]