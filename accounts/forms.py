from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job, Interview

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', 'student')  # default role
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.role
        if commit:
            user.save()
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'criteria', 'vacancies']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['application', 'scheduled_at', 'meeting_link', 'notes']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }