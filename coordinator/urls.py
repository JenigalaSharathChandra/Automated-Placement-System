# ✅ coordinator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('approve-jobs/', views.approve_jobs, name='approve_jobs'),
    path('job-status/<int:job_id>/', views.update_job_status, name='update_job_status'),  # ✅ Corrected line
    path('monitor-applications/', views.monitor_applications, name='monitor_applications'),
]