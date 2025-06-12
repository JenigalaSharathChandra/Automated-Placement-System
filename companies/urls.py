# ✅ companies/urls.py

from django.urls import path
from . import views
from .views import recruiter_student_profile

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('view-applicants/', views.view_applicants, name='view_applicants'),
    path('update-status/', views.update_application_status, name='update_application_status'),
    path('schedule-interviews/', views.schedule_interviews, name='schedule_interviews'),
    path('schedule-interview/<int:application_id>/', views.schedule_interview_form, name='schedule_interview_form'),
    path('edit-interview/<int:interview_id>/', views.edit_interview, name='edit_interview'),
    path('update-interview-status/<int:interview_id>/', views.update_interview_status, name='update_interview_status'),
    path('delete-interview/<int:interview_id>/', views.delete_interview, name='delete_interview'),
    path('company/student-profile/<int:student_id>/', recruiter_student_profile, name='recruiter_student_profile'),
] 