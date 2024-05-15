
from django.shortcuts import render, redirect, HttpResponse
from .forms import*
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from job.models import *
from job.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required
from job.decoratore import is_recruiter
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

@is_recruiter
def rec_header(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    recruiter=Recruiter.objects.get(user=user.id)
    return render(request,'Recruiter/headers.html',{'user':user,'profile':profile,'recruiter':recruiter})


def job_detail(request,id):
    job=Job.objects.get(id=id)
    user=request.user
    profile=Profile.objects.get(user=user.id)
    return render(request,'Recruiter/job_detail.html',{'job':job,'user':user,'profile':profile})


@is_recruiter
def recruiter_home(request):
    #job post form
    user = request.user
    profile = Profile.objects.get(user=user)
    recruiter = Recruiter.objects.get(user=profile)
    job=Job.objects.filter(recruiter=recruiter)[0:3]
    no_post=Job.objects.filter(recruiter=recruiter).count()
    category=Job_category.objects.all()
    return render(request,'Recruiter/Recruiter_home.html',{'user':user,'recruiter':recruiter,'job':job,'no_post':no_post,'category':category})

@is_recruiter
def recruiter_dashboard(request):
    # Check if the user is authenticated and has a profile associated with them
    if request.user.is_authenticated:
        try:
            # Access the associated Profile instance
            profile = request.user.profile
            # Check the is_recruiter attribute
            if profile.is_recruiter:
                # Code for the recruiter dashboard
                return HttpResponse('Recruiter Dashboard')
            else:
                return HttpResponse('You are Applicant')
        except Profile.DoesNotExist:
            # Handle the case where no Profile instance is associated with the user
            return HttpResponse('lNo or')
    else:
        return redirect('login')
    
def recruiter_profile(request):
    form = RecruiterForm()
    if request.method == 'POST':
        form = RecruiterForm(request.POST, request.FILES)
        if form.is_valid():
            profile = Profile.objects.create(user=request.user)  # Create a Profile instance for the user
            recruiter_instance = form.save(commit=False)
            recruiter_instance.user = profile  # Assign the profile to the recruiter instance
            recruiter_instance.save()
            return redirect('home')
          
    context = {'form': form}
    return render(request, 'recruiter.html', context)


def profile(request,username):
    user=request.user
    profile = Profile.objects.get(user=user,name=username)
    recruiter=Recruiter.objects.get(user=profile)
    context={
        'profile':profile,'recruiter':recruiter
    }
    print(username)
    return render(request,'Recruiter/rec_profile.html',context)

@is_recruiter
def job_create(request):
    user=request.user
    profile = Profile.objects.get(user=user)
    recruiter = Recruiter.objects.get(user=profile)
    form = JobForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter =recruiter
            job.save()
            return redirect('home')
    context = {'form': form,'recruiter':recruiter}
    return render(request, 'job_create.html', context)

@is_recruiter
def candidate_list(request,id):
    user=request.user
    profile = Profile.objects.get(user=user)
    applicant=ApplicantProfile.objects.all()
    recruiter = Recruiter.objects.get(user=profile)
    job=Job.objects.get(recruiter=recruiter,id=id)
    #applied person for the job list
    apply = Apply.objects.filter(job=job)
    #get the candidate list
    candidates = apply.values_list('candidate_detail', flat=True)
    candidate_profiles = ApplicantProfile.objects.filter(id__in=apply.values_list('candidate_detail_id', flat=True))
    
    # Count the number of candidates
    c_len = candidate_profiles.count()
    can_skill=Skill.objects.filter(profile__in=candidate_profiles)
    print(can_skill)
    paginator = Paginator(candidate_profiles, 20)
    page_number = request.GET.get('page')
    candidate_profiles_paginated = paginator.get_page(page_number)
    # Count the total number of candidates
    total_candidates = paginator.count
    # Get the skills associated with candidate profiles
    candidate_skills = Skill.objects.filter(profile__in=candidate_profiles_paginated)

    #add searching and sorting functionality

    if 'search' in request.GET:
     search_term = request.GET['search']
     candidate_profiles = candidate_profiles.filter(user__name__icontains=search_term)

    if 'sort' in request.GET:
     sort_term = request.GET['sort']
     if sort_term == 'name':
        candidate_profiles = candidate_profiles.order_by('user__name')
     elif sort_term == 'experience':
        # Assuming 'experience' refers to the 'experience' field in ApplicantProfile model
        candidate_profiles = candidate_profiles.order_by('-experience')

    return render(request,'Recruiter/candidate_list.html',{'job':job,'recruiter':recruiter,'profile':profile,'candidates':candidates,'c_len':c_len,'candidate_profiles':candidate_profiles,'can_skill':can_skill,'candidate_profiles_paginated':candidate_profiles_paginated,'total_candidates':total_candidates,'candidate_skills':candidate_skills})

@is_recruiter
def rec_job(request):
    user=request.user
    profile = Profile.objects.get(user=user)
    recruiter = Recruiter.objects.get(user=profile)
    job=Job.objects.filter(recruiter=recruiter)
    return render(request,'Recruiter/recruiter-job.html',{'job':job,'recruiter':recruiter})


def rec_job_list(request):
    jobs=Job.objects.all()
    user=request.user
    profile = Profile.objects.get(user=user)
    recruiter = Recruiter.objects.get(user=profile)
    return render(request,'Recruiter/rec_joblist.html',{'jobs':jobs,'recruiter':recruiter,'profile':profile})



def candidate_profile(request,username):
    profile = Profile.objects.get(name=username)
    
    applicant = ApplicantProfile.objects.get(user=profile)
    skills = Skill.objects.filter(profile=applicant)
    education = Education.objects.filter(profile=applicant)
    links=addLink.objects.filter(profile=applicant)
    projects=Project.objects.filter(profile=applicant)
    experience = Experience.objects.filter(userprofile=applicant)
    achievements=achievement.objects.filter(userprofile=applicant)
    form = JobStatus(request.POST or None) 
    status = None
     # Initialize the form
    user=request.user
    profile = Profile.objects.get(user=user)
    recruiter = Recruiter.objects.get(user=profile)

    return render(request, 'Recruiter/candidate_profile.html', { 'applicant': applicant, 'skill': skills, 'education': education, 'experience': experience, 'profile': profile,'links':links,'achievements':achievements,'projects':projects,'recruiter':recruiter})
   

# Import the necessary modules


# Define the constant username
CONSTANT_USERNAME = "John Doe"  # Replace "John Doe" with the desired constant username

# Define the view function to send email
def send_email(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')  # Assuming you're sending email as a POST parameter
        
        if email:
            # Long message content with constant username
            message = (
                f"Dear {CONSTANT_USERNAME},\n\n"
                "Congratulations! We are pleased to inform you that you have been shortlisted for further evaluation.\n\n"
                "Please find attached the details of the next steps in the selection process.\n\n"
                "Best regards,\n"
                "Your Company"
            )
            
            # Send the email
            send_mail('Congratulations! You have been shortlisted', message, settings.EMAIL_HOST_USER, [email])
            
            return HttpResponse('Email sent successfully!')
        else:
            return HttpResponse('Email address not provided')
    else:
        return HttpResponse('Invalid request method')
