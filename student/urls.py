# ✅ student/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('view-jobs/', views.view_jobs, name='view_jobs'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
    path('profile/', views.profile, name='profile'),
    path('upcoming-interviews/', views.upcoming_interviews, name='upcoming_interviews'),
]