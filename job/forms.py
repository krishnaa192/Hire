
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *




class CandidateSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

class CandidateLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'is_recruiter', 'is_applicant']

      

class CandidateForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        # fields = '__all__'
        fields=['bio','phone','is_recruiter','is_applicant','is_fresher','experience','resume']

        widgets = {
            'is_recruiter': HiddenInput()
        }
          
        # fields = ['phone', 'experience', 'current_ctc', 'expected_ctc', 'graduated_from', 'degree', 'skills', 'resume']

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['job', 'candidate_detail', 'recruiter_detail', 'about']
        widgets = {
            'job': forms.HiddenInput(),
            'candidate_detail': forms.HiddenInput(),
            'recruiter_detail': forms.HiddenInput(),
            'profile': forms.HiddenInput(),
        }


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        exclude = ['is_recruiter','is_applicant']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['profile']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['profile']

class AchievementForm(forms.ModelForm):
    class Meta:
        model=achievement
        exclude = ['userprofile']
       



class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = ['profile','level']
       
class AddLinkForm(forms.ModelForm):
    class Meta:
        model = addLink
        exclude = ['profile']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['profile']
