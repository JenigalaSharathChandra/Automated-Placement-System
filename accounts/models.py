from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('recruiter', 'Company Recruiter'),
        ('coordinator', 'Placement Coordinator'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    skills = models.CharField(max_length=255, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    achievements = models.TextField(blank=True)       # ✅ new
    projects = models.TextField(blank=True)           # ✅ new
    certifications = models.TextField(blank=True)     # ✅ new

    def __str__(self):
        return self.user.username

class CompanyRecruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.company_name})"

class PlacementCoordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(CompanyRecruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    criteria = models.CharField(max_length=100)
    vacancies = models.IntegerField()

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.title} - {self.recruiter.company_name}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} → {self.job.title}"

User = get_user_model()

class SystemLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.action}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"

class Interview(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Interview for {self.application.student.user.username} - {self.application.job.title}"
