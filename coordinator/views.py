# ✅ Refactored Coordinator App - coordinator/views.py

from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import coordinator_required
from accounts.models import Job, Application, Interview

@coordinator_required
def coordinator_dashboard(request):
    pending_jobs_count = Job.objects.filter(approved=False).count()
    total_applications = Application.objects.count()
    return render(request, 'coordinator/dashboard.html', {
        'pending_jobs_count': pending_jobs_count,
        'total_applications': total_applications,
    })

@coordinator_required
def approve_jobs(request):
    pending_jobs = Job.objects.filter(approved=False)
    return render(request, 'coordinator/approve_jobs.html', {'jobs': pending_jobs})

@coordinator_required
def approve_job_action(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.approved = True
    job.save()
    return redirect('approve_jobs')

@coordinator_required
def monitor_applications(request):
    applications = Application.objects.select_related('student__user', 'job__recruiter__user')
    return render(request, 'coordinator/monitor_applications.html', {'applications': applications})
