
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from job.models import *
from .models import *




class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        # fields = '__all__'
        fields = ['is_recruiter','is_applicant' ,'company_name', 'logo', 'about_company', 'company_address', 'company_website', 'company_email','grade']
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



class Recruiting(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['company_name','logo','about_company','company_address','company_website','company_email','grade']
        widgets = {
            'company_name': forms.TextInput(attrs={'class':'form-control'}),
            'logo': forms.FileInput(attrs={'class':'form-control'}),
            'about_company': forms.Textarea(attrs={'class':'form-control'}),
            'company_address': forms.TextInput(attrs={'class':'form-control'}),
            'company_website': forms.TextInput(attrs={'class':'form-control'}),
            'company_email': forms.EmailInput(attrs={'class':'form-control'}),
            
            'grade': forms.Select(attrs={'class':'form-control'}),
        }
