
from django.shortcuts import render, redirect, HttpResponse
from .forms import*
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from job.models import *
from job.forms import *
from .forms import *
from django.contrib.auth.decorators import login_required
from job.decoratore import is_recruiter


@is_recruiter
def rec_header(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    recruiter=Recruiter.objects.get(user=user.id)
    return render(request,'Recruiter/headers.html',{'user':user,'profile':profile,'recruiter':recruiter})

@is_recruiter
def recruiter_home(request):
    #job post form
    user=request.user
    profile=Profile.objects.get(user=user.id)
    recruiter=Recruiter.objects.get(user=user.id)
    job=Job.objects.filter(recruiter=recruiter)[0:3]
    no_post=Job.objects.filter(recruiter=recruiter).count()
    category=Job_category.objects.filter()
    return render(request,'Recruiter/Recruiter_home.html',{'user':user,'profile':profile,'recruiter':recruiter,'job':job,'no_post':no_post,'category':category})

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
    

@is_recruiter
def recruiter_profile(request):
    form = RecruiterForm()
    if request.method == 'POST':
        form = RecruiterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'recruiter.html', context)


@is_recruiter
def job_create(request):
    user=request.user
    recruiter=Recruiter.objects.get(user=user.id)
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
def candidate_list(request):
    user=request.user
    recruiter=Recruiter.objects.get(user=user.id)
    job=Job.objects.filter(recruiter=recruiter)
    return render(request,'Recruiter/candidate_list.html',{'job':job})

@is_recruiter
def rec_job(request):
    user=request.user
    recruiter=Recruiter.objects.get(user=user.id)
    job=Job.objects.filter(recruiter=recruiter)
    return render(request,'Recruiter/recruiter-job.html',{'job':job,'recruiter':recruiter})