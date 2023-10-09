from django.shortcuts import render, redirect, HttpResponse
from .forms import*
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from .decoratore import is_recruiter,is_applicant
# Create your views here.





def profile(request):
    profile = request.user
    form = ProfileForm() 
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the user
            profile.save()
            return redirect('applicant_profile')
    # else:
           
    #     form = ProfileForm(instance=profile)
  
    return render(request,'signup2.html', {'form':form})
def welcome(request):
    return render(request,'index.html')
def recruiter_home(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    recruiter=Recruiter.objects.get(user=user.id)

    return render(request,'recruiter_dashboard.html',{'user':user,'profile':profile,'recruiter':recruiter})

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
    
def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
           
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile') 
    else:
        form = CandidateSignupForm()
    return render(request, 'signup.html', {'form': form})

def candidate_login(request):
    if request.method == 'POST':
        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the candidate profile page after login
    else:
        form = CandidateLoginForm()
    return render(request, 'logins.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def candidate_profile(request):
    form = CandidateForm()
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'candidate_profile.html', context)


@login_required(login_url='login')
def recruiter_profile(request):
    form = RecruiterForm()
    if request.method == 'POST':
        form = RecruiterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'recruiter.html', context)


def job_detail(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job': job}
    return render(request, 'job-detail.html', context)

def apply_job(request, pk):
    #getting logged in user
    user = request.user
    profile=Profile.objects.get(user=user.id)
    job = Job.objects.get(pk=pk)
    #getting logged in user profile of candidate
    candidate=ApplicantProfile.objects.get(pk=pk)

    # candidate=Candidate.objects.get()
    recruiter=ApplicantProfile.objects.get(pk=job.recruiter.company_id)  

    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            appli = form.save(commit=False)
            appli.job = job
            appli.save()
             # Sending email notification
            subject = 'Job Application'
            message = f'A new application has been submitted for the job "{job.title}" by {profile.name}.'
            from_email = 'krisna.upadhyayyy@gmail.com'  # Set your 'from' email address here
            recipient_list = [profile.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('verifications_job')
            
            #save the profile in databse
    else:
               
        form = ApplyForm(initial={
            'job': job.id,
            'candidate_detail': candidate.id,
            'recruiter_detail': recruiter.company_id,
        })

    context = {'job': job, 'form': form, 'candidate': candidate, 'recruiter': recruiter, 'profile': profile}
    return render(request, 'apply_form.html', context)

def verifications_job(request):
    return render(request,'job_verification.html')

def about(request):
    return render(request,'about.html')

def home(request):

 if not request.user.is_authenticated:
        return redirect('welcome')
 elif request.user.is_authenticated and request.user.profile.is_recruiter:
       return redirect('recruiter_home')  

 else:
    # user = request.user
    # applied_jobs = Apply.objects.filter(profile=user.profile).values_list('job', flat=True)
    jobs = Job.objects.all()
   
   #add logic that if user is appplied for a job then it should not be shown in the list of jobs
    profile=ApplicantProfile.objects.all()
    usr=Profile.objects.all()
    category=Job_category.objects.all()
    skill=Skill.objects.all()
     # Handling search logic
    query = request.GET.get('q')
    if query:
         jobs = jobs.filter(
            Q(experience__icontains=query) |
            Q(location__icontains=query) |
            Q(job_type__icontains=query)| 
             Q(skills__icontains=query) 
        ).distinct()
    #handling that after applying to a job it should not be shown in the list  
    # Handling sort logic
    sort_by = request.GET.get('sort')
    if sort_by == 'experience_asc':
        jobs = jobs.order_by('experience')
    elif sort_by == 'experience_desc':
        jobs = jobs.order_by('-experience')
    elif sort_by == 'full_time':
        jobs = jobs.filter(job_type='Full Time')
    elif sort_by == 'part_time':
        jobs = jobs.filter(job_type='Part Time')
    elif sort_by == 'internship':
        jobs = jobs.filter(job_type='Internship')
    elif sort_by == 'salary_asc':
        jobs = jobs.order_by('salary')
    elif sort_by == 'salary_desc':
        jobs = jobs.order_by('-salary')
    elif sort_by == 'posted_on_asc':
        jobs = jobs.order_by('posted_on')
    elif sort_by == 'posted_on_desc':
        jobs = jobs.order_by('-posted_on')
    
    location_filter = request.GET.get('location')
    if location_filter:
     jobs = jobs.filter(location=location_filter)
     

    context = {'jobs': jobs,'profile':profile,'usr':usr,'skill':skill,'category':category}
    return render(request,'home.html',context)
 
def job_list(request):
    jobs = Job.objects.all()
   
   #add logic that if user is appplied for a job then it should not be shown in the list of jobs
    profile=ApplicantProfile.objects.all()
    usr=Profile.objects.all()
    skill=Skill.objects.all()
     # Handling search logic
    query = request.GET.get('q')
    if query:
         jobs = jobs.filter(
            Q(experience__icontains=query) |
            Q(location__icontains=query) |
            Q(job_type__icontains=query)| 
             Q(skills__icontains=query) 
        ).distinct()
    #handling that after applying to a job it should not be shown in the list  
    # Handling sort logic
    sort_by = request.GET.get('sort')
    if sort_by == 'experience_asc':
        jobs = jobs.order_by('experience')
    elif sort_by == 'experience_desc':
        jobs = jobs.order_by('-experience')
    elif sort_by == 'full_time':
        jobs = jobs.filter(job_type='Full Time')
    elif sort_by == 'part_time':
        jobs = jobs.filter(job_type='Part Time')
    elif sort_by == 'internship':
        jobs = jobs.filter(job_type='Internship')
    elif sort_by == 'salary_asc':
        jobs = jobs.order_by('salary')
    elif sort_by == 'salary_desc':
        jobs = jobs.order_by('-salary')
    elif sort_by == 'posted_on_asc':
        jobs = jobs.order_by('posted_on')
    elif sort_by == 'posted_on_desc':
        jobs = jobs.order_by('-posted_on')
    
    location_filter = request.GET.get('location')
    if location_filter:
     jobs = jobs.filter(location=location_filter)
     
    context = {'jobs': jobs,'profile':profile,'usr':usr,'skill':skill}
    return render(request, 'job-list.html', context)

def user_profile(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    # skill=Skill.objects.get(user=user)
    context={'profile':profile,'candidate':candidate,}
    return render(request,'user_profile.html',context)

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
    context = {'form': form}
    return render(request, 'job_create.html', context)


def update_profile(request):
    return render(request,'profile_setting.html')


def applicant_profile(request):
    user = request.user
    form=ApplicantProfileForm()
    try:
        profile = Profile.objects.get(user=user)
        # applicant_profile = ApplicantProfile.objects.get(user=profile)
    except Profile.DoesNotExist:
        profile = None
        applicant_profile = None
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES)
        if form.is_valid():
            applicant_profile = form.save(commit=False)
            applicant_profile.user = user.profile  
            applicant_profile.save()
            if profile is not None:
                profile.applicantprofile = applicant_profile
                profile.save()
            return redirect('home')
    else:
        form = ApplicantProfileForm()

    context = {'form': form}
    return render(request, 'applicant_profile.html', context)

def update_applicant_profile(request):
    user = request.user
    form=ApplicantProfileForm()
    profile = Profile.objects.get(user=user)
    applicant_profile = ApplicantProfile.objects.get(user=profile)
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES,instance=applicant_profile)
        if form.is_valid():
            applicant_profile = form.save(commit=False)
            applicant_profile.user = user.profile  
            applicant_profile.save()
            if profile is not None:
                profile.applicantprofile = applicant_profile
                profile.save()
            return redirect('user_profile')
    else:
        form = ApplicantProfileForm(instance=applicant_profile)

    context = {'form': form}
    return render(request, 'update_applicant_profile.html', context)

def education(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    education=Education.objects.filter(profile=candidate)
    form=EducationForm()
    if  request.method=='POST':
        form=EducationForm(request.POST)
        if form.is_valid():
            education=form.save(commit=False)
            education.profile=candidate
            education.save()
            return redirect('home')
    context={'profile':profile,'candidate':candidate,'education':education,'form':form}
    return render(request,'education.html',context)

def update_education(request,pk):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    education=Education.objects.get(pk=pk)
    form=EducationForm(instance=education)
    if  request.method=='POST':
        form=EducationForm(request.POST,instance=education)
        if form.is_valid():
            education=form.save(commit=False)
            education.profile=candidate
            education.save()
            return redirect('home')
    context={'profile':profile,'candidate':candidate,'education':education,'form':form}
    return render(request,'update_education.html',context)

def project(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    project=Project.objects.filter(profile=candidate)
    form=ProjectForm()
    if  request.method=='POST':
        form=ProjectForm(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            project.profile=candidate
            project.save()
            return redirect('home')
    context={'profile':profile,'candidate':candidate,'project':project,'form':form}
    return render(request,'project.html',context)

def update_project(request,pk):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    project=Project.objects.get(pk=pk)
    form=ProjectForm(instance=project)
    if  request.method=='POST':
        form=ProjectForm(request.POST,instance=project)
        if form.is_valid():
            project=form.save(commit=False)
            project.profile=candidate
            project.save()
            return redirect('home')
    context={'profile':profile,'candidate':candidate,'project':project,'form':form}
    return render(request,'update_project.html',context)