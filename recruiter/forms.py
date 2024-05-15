
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from job.models import *




class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        # fields = '__all__'
        fields = ['is_recruiter','is_applicant' ,'company_name', 'logo', 'about_company', 'company_address', 'company_website', 'company_email', 'recruting_face','grade']
        widgets = {
            'is_applicant': HiddenInput()
        }



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['recruiter']

class JobStatus(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['job_status']