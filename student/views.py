from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.decorators import student_required
from accounts.models import Job, Application, Interview, Student

# Utility to calculate profile completion
def calculate_profile_completion(student):
    fields = [
        student.name, student.skills, student.linkedin, student.github,
        student.bio, student.achievements, student.projects, student.certifications,
        student.gpa
    ]
    filled = sum(1 for field in fields if field)
    return int((filled / len(fields)) * 100)

@student_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)

    total_jobs = Job.objects.filter(status='approved').count()
    applied_jobs = Application.objects.filter(student=student).count()
    upcoming_interviews_count = Interview.objects.filter(
        application__student=student,
        scheduled_at__gte=timezone.now()
    ).count()

    profile_completion = calculate_profile_completion(student)

    upcoming_interview_obj = Interview.objects.filter(
        application__student=student,
        scheduled_at__gte=timezone.now()
    ).select_related('application__job__recruiter').order_by('scheduled_at').first()

    company_name = upcoming_interview_obj.application.job.recruiter.company_name if upcoming_interview_obj else None
    job_title = upcoming_interview_obj.application.job.title if upcoming_interview_obj else None

    return render(request, 'student/dashboard.html', {
        'total_jobs': total_jobs,
        'applied_jobs': applied_jobs,
        'upcoming_interviews': upcoming_interviews_count,
        'profile_completion': profile_completion,
        'company_name': company_name,
        'job_title': job_title,
    })

@student_required
def view_jobs(request):
    student = Student.objects.get(user=request.user)
    approved_jobs = Job.objects.filter(status='approved').select_related('recruiter')

    title_query = request.GET.get('title', '')
    company_query = request.GET.get('company', '')
    min_vacancies = request.GET.get('vacancies', '')

    if title_query:
        approved_jobs = approved_jobs.filter(title__icontains=title_query)
    if company_query:
        approved_jobs = approved_jobs.filter(recruiter__company_name__icontains=company_query)
    if min_vacancies:
        try:
            approved_jobs = approved_jobs.filter(vacancies__gte=int(min_vacancies))
        except ValueError:
            pass

    sort_by = request.GET.get('sort_by')
    if sort_by == 'title_asc':
        approved_jobs = approved_jobs.order_by('title')
    elif sort_by == 'title_desc':
        approved_jobs = approved_jobs.order_by('-title')
    elif sort_by == 'vacancies_asc':
        approved_jobs = approved_jobs.order_by('vacancies')
    elif sort_by == 'vacancies_desc':
        approved_jobs = approved_jobs.order_by('-vacancies')

    applied_job_ids = Application.objects.filter(student=student).values_list('job_id', flat=True)

    paginator = Paginator(approved_jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/view_jobs.html', {
        'page_obj': page_obj,
        'applied_job_ids': applied_job_ids,
        'title_query': title_query,
        'company_query': company_query,
        'min_vacancies': min_vacancies,
        'sort_by': sort_by,
    })

@student_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='approved')
    student = get_object_or_404(Student, user=request.user)
    existing_application = Application.objects.filter(student=student, job=job).first()

    if existing_application:
        messages.info(request, "You have already applied to this job.")
    else:
        Application.objects.create(student=student, job=job)
        messages.success(request, "Application submitted successfully.")

    return redirect('view_jobs')

@student_required
def applied_jobs(request):
    student = get_object_or_404(Student, user=request.user)
    applications = Application.objects.filter(student=student).select_related('job__recruiter')

    paginator = Paginator(applications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/applied_jobs.html', {'page_obj': page_obj})

@student_required
def profile(request):
    student = request.user.student

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        skills = request.POST.get('skills')
        gpa_input = request.POST.get('gpa')
        linkedin = request.POST.get('linkedin')
        github = request.POST.get('github')
        bio = request.POST.get('bio')
        achievements = request.POST.get('achievements')
        projects = request.POST.get('projects')
        certifications = request.POST.get('certifications')

        student.name = name
        student.skills = skills
        student.linkedin = linkedin
        student.github = github
        student.bio = bio
        student.achievements = achievements
        student.projects = projects
        student.certifications = certifications

        try:
            student.gpa = float(gpa_input) if gpa_input and gpa_input.lower() != 'none' else None
        except ValueError:
            student.gpa = None

        request.user.email = email
        request.user.save()
        student.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'student/profile.html', {
        'student': student,
        'achievements_list': student.achievements.splitlines() if student.achievements else [],
        'projects_list': student.projects.splitlines() if student.projects else [],
        'certifications_list': student.certifications.splitlines() if student.certifications else [],
    })

@student_required
def upcoming_interviews(request):
    student = Student.objects.get(user=request.user)
    interviews = Interview.objects.filter(
        application__student=student
    ).select_related('application__job').order_by('scheduled_at')

    paginator = Paginator(interviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/upcoming_interviews.html', {'page_obj': page_obj})
