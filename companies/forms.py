from django import forms
from accounts.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'criteria', 'vacancies']
