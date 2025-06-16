from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from accounts.decorators import coordinator_required
from accounts.models import Job, Application

@coordinator_required
def coordinator_dashboard(request):
    pending_jobs_count = Job.objects.filter(status='pending').count()
    total_applications = Application.objects.count()

    # For Pie Chart - count jobs by status
    status_counts = {
        'approved': Job.objects.filter(status='approved').count(),
        'pending': Job.objects.filter(status='pending').count(),
        'rejected': Job.objects.filter(status='rejected').count(),
    }

    # Recent Activities - latest 5 applications
    recent_activities = Application.objects.select_related('student__user', 'job').order_by('-applied_at')[:5]

    return render(request, 'coordinator/dashboard.html', {
        'pending_jobs_count': pending_jobs_count,
        'total_applications': total_applications,
        'status_counts': status_counts,
        'recent_activities': recent_activities,
    })

@coordinator_required
def approve_jobs(request):
    pending_jobs = Job.objects.filter(status='pending')
    return render(request, 'coordinator/approve_jobs.html', {'jobs': pending_jobs})

@require_POST
@coordinator_required
def update_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    new_status = request.POST.get('status')

    if new_status in ['approved', 'rejected']:
        job.status = new_status
        job.save()

    return redirect('approve_jobs')

@coordinator_required
def monitor_applications(request):
    applications = Application.objects.select_related('student__user', 'job__recruiter__user')
    return render(request, 'coordinator/monitor_applications.html', {'applications': applications})
