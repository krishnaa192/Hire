from django.shortcuts import render, redirect, HttpResponse
from .forms import*
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from recruiter.models import *
from recruiter.forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from .decoratore import is_recruiter,is_applicant
from django.core.paginator import Paginator
# Create your views here.

def header(request):
    user=request.user
    applicant=ApplicantProfile.objects.get(user=user.id)
    context={'applicant':applicant}
    return render(request,'header.html',context)




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
    return render(request,'signup2.html', {'form':form})

def welcome(request):
    
    return render(request,'index.html')

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
                if user.profile.is_applicant:
                 login(request, user)
                 return redirect('home')
                else:
                    return redirect('recruiter_home')  # Redirect to the candidate profile page after login
    else:
        form = CandidateLoginForm()
    return render(request, 'logins.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('welcome')


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





def job_detail(request, pk):
    job = Job.objects.get(id=pk)
 
    applicant=ApplicantProfile.objects.get(user=request.user.id)
    context = {'job': job,'applicant':applicant}
    return render(request, 'job-detail.html', context)

@login_required(login_url='login')
def apply_job(request, pk):
    user = request.user
    applicant=ApplicantProfile.objects.get(user=user.id)
    #check whter user is appplied for a job or not
    if Apply.objects.filter(candidate_detail=applicant,job=pk).exists():
        return redirect('home')
    profile=Profile.objects.get(user=user.id)
    job = Job.objects.get(pk=pk)
    #getting logged in user profile of candidate
    candidate=ApplicantProfile.objects.get(user=profile)
    # candidate=Candidate.objects.get()
    recruiter=Recruiter.objects.get(pk=job.recruiter.pk)  
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
            return redirect('home')
    else:       
        form = ApplyForm(initial={
            'job': job.id,
            'candidate_detail': candidate.id,
            'recruiter_detail': recruiter
        })

    context = {'job': job, 'form': form, 'candidate': candidate, 'recruiter': recruiter, 'profile': profile}
    return render(request, 'apply_form.html', context)


def about(request):
    return render(request,'about.html')


@is_applicant
def home(request):
 if not request.user.is_authenticated:
        return redirect('welcome')
 elif request.user.is_authenticated and request.user.profile.is_recruiter:
       return redirect('recruiter_home')  
 else:
    jobs = Job.objects.all()
    profile=request.user.profile
    category=Job_category.objects.all()
    skill=Skill.objects.all()
    applicant=ApplicantProfile.objects.get(user=profile)
    applied_jobs = Apply.objects.filter(candidate_detail=applicant).values('job')
    jobs = jobs.exclude(id__in=applied_jobs)
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
     
    jobs = jobs[0:4]
   
    context = {'jobs': jobs,'profile':profile,'skill':skill,'category':category,'applicant':applicant}
    return render(request,'home.html',context)


def job_list(request):
    profile = request.user.profile
    applicant = ApplicantProfile.objects.get(user=profile)
    applied_jobs = Apply.objects.filter(candidate_detail=applicant).values('job')
    jobs = Job.objects.exclude(id__in=applied_jobs)
 
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(experience__icontains=query) |
            Q(location__icontains=query) |
            Q(job_type__icontains=query) |
            Q(skills__icontains=query)
        ).distinct()

    
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

    # Handle location filter
    location_filter = request.GET.get('location')
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    # Create a paginator
    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    jobs = jobs[0:4]
    context = {
        'jobs': jobs,  # Use the paginated jobs here
        'profile': profile,
        'page': page,
        'applicant': applicant,
    }
    
    return render(request, 'job-list.html', context)

@is_applicant
def user_profile(request):
    user=request.user
    applicant=ApplicantProfile.objects.get(user=user.id)
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    skill=Skill.objects.filter(profile=applicant.id)
    education=Education.objects.filter(profile=applicant.id)
    project=Project.objects.filter(profile=applicant.id)
    link=addLink.objects.filter(profile=applicant.id)
    context={'profile':profile,'candidate':candidate,'applicant':applicant,'skill':skill,'education':education,'project':project,'link':link}
    return render(request,'profilepage.html',context)



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
            return redirect('user_profile')
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
            return redirect('user_profile')
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
            return redirect('user_profile')
    context={'profile':profile,'candidate':candidate,'education':education,'form':form}
    return render(request,'update_education.html',context)

def delete_education(request,pk):
    education=Education.objects.get(pk=pk)
    education.delete()
    return redirect('user_profile')



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
            return redirect('user_profile')
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
            return redirect('user_profile')
    context={'profile':profile,'candidate':candidate,'project':project,'form':form}
    return render(request,'update_project.html',context)


def delete_project(request,pk):
    project=Project.objects.get(pk=pk)
    project.delete()
    return redirect('user_profile')


def add_skill(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    skill=Skill.objects.filter(profile=candidate)
    form=SkillForm()
    if  request.method=='POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.profile=candidate
            skill.save()
            return redirect('user_profile')
    context={'profile':profile,'candidate':candidate,'skill':skill,'form':form}
    return render(request,'profilepage.html',context) 

def delete_skill(request,pk):
    skill=Skill.objects.get(pk=pk)
    skill.delete()
    return redirect('user_profile')


def addlink(request):
    user=request.user
    profile=Profile.objects.get(user=user.id)
    candidate=ApplicantProfile.objects.get(user=profile)
    form=AddLinkForm(request.POST,request.FILES)
    if request.method=='POST':
        form=AddLinkForm(request.POST,request.FILES)
        if form.is_valid():
            skill_name = form.cleaned_data['name']

    
            existing_skill = Skill.objects.filter(name=skill_name).first()

            if not existing_skill:
                # If no skill with the same name exists, save the new skill
                skill = form.save(commit=False)
                skill.profile = candidate
                skill.save()
            return redirect('user_profile')
    context={'profile':profile,'candidate':candidate,'form':form}
    return render(request,'addlink.html',context)
        
def deleteLink(request,pk):
    link=addLink.objects.get(pk=pk)
    link.delete()
    return redirect('user_profile')

def category(request,cat):
    cats=Job_category.objects.get(category=cat)
    cat_job=Job.objects.filter(category=cats) 
    context={'cat_job':cat_job,'cats':cats}
    return render(request,'categories.html',context) 



@login_required(login_url='login')
def inbox(request):
     user=request.user
     profile=request.user.profile
     messagesent=Message.objects.filter(receiver=profile)
     applicant=ApplicantProfile.objects.get(user=user.id)
     unreadmessages=messagesent.filter(is_read=False)
     count=unreadmessages.count()
     context={'messagesent':messagesent,'profile':profile,'count':count,'applicant':applicant}
     return render(request,'message.html',context)


def SendMessage(request,pk):
    profile=request.user.profile
    receiver=Profile.objects.get(pk=pk)
    messagesent=Message.objects.filter(receiver=profile)
    form=SendMessageForm()
    if request.method=='POST':
        form=SendMessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender=profile
            message.save()
            return redirect('/')
    context={'form':form,'receiver':receiver,'profile':profile,'messagesent':messagesent}
    return render(request,'sent.html',context)


def view_msg(request,pk):
    profile=request.user.profile
    receiver=Profile.objects.get(pk=pk)
    messagesent=Message.objects.filter(receiver=profile)
    form=SendMessageForm()
    if request.method=='POST':
        form=SendMessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender=profile
            message.save()
            return redirect('/')
    context={'form':form,'receiver':receiver,'profile':profile,'messagesent':messagesent}
    return render(request,'usermsg.html',context)