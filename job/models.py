from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings



class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ApplicantProfile(models.Model):
    highrt_qualification=[
        ('B.Tech','B.Tech'),
        ('B.E','B.E'),
        ('B.Sc','B.Sc'),
        ('B.Com','B.Com'),
        ('B.A','B.A'),
        ('M.Tech','M.Tech'),
        ('M.E','M.E'),
        ('M.Sc','M.Sc'),
        ('M.Com','M.Com'),
        ('M.A','M.A'),
        ('Phd','Phd'),
        ('Diploma','Diploma'),
    ]
    user=models.OneToOneField(Profile,on_delete=models.CASCADE)
    bio=models.TextField()
    phone=models.IntegerField()
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=True)
    is_fresher=models.BooleanField(default=False)
    experience = models.CharField(max_length=100,default=0)
    profile_pic = models.ImageField(upload_to='image/profile')
    resume = models.FileField(upload_to='resume', null=True, blank=True)
    highest_qualification=models.CharField(max_length=100,choices=highrt_qualification)
    address=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)


    # how assign name from profile model
    



    def __str__(self):
        return self.user.name









class Recruiter(models.Model):
    #grade c:3lpa to 7lpa and for internship 4k to 12k
    #grade b:7lpa to 18lpa and for internship 12k to 40k
    #grade a:18lpa to 50lpa and for internship 40k to 2lacs
    #grade A+:50lpa+ and for internship 2lacs+ 
    grade=[
        ('A','A'),
        ('B','B'),
        ('C','C'),
    ]
    user=models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='recruiter')
    company_id=models.AutoField(primary_key=True)
    is_recruiter = models.BooleanField(default=True)
    is_applicant = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo')
    about_company = models.TextField()
    company_address = models.CharField(max_length=100)
    company_website = models.CharField(max_length=100)
    company_email = models.CharField(max_length=100)
    grade=models.CharField(max_length=100,choices=grade)

    def __str__(self):
        return self.company_name





class Job_category(models.Model):
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.category
    

class Job(models.Model):
    id=models.AutoField(primary_key=True)
    job_types=[
        ('Full Time','Full Time'),
        ('Part Time','Part Time'),
        ('Internship','Internship'),
        ('other','other')
    ]
    deadline=models.DateField(null=True,blank=True)
    Responsibilities=models.TextField(null=True,blank=True)
    Qualifications=models.TextField(null=True,blank=True)
    category=models.ForeignKey(Job_category,on_delete=models.CASCADE,null=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=22)
    posted_on = models.DateTimeField(auto_now_add=True)
    experience = models.CharField(max_length=100)
    job_type=models.CharField(choices=job_types,max_length=100)
    vacancy=models.IntegerField( default=1)
    category=models.ForeignKey(Job_category,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.title

class Education(models.Model):
    degree=[
        ('B.Tech','B.Tech'),
        ('B.E','B.E'),
        ('B.Sc','B.Sc'),
        ('B.Com','B.Com'),
        ('B.A','B.A'),
        ('M.Tech','M.Tech'),
        ('M.E','M.E'),
        ('M.Sc','M.Sc'),
        ('M.Com','M.Com'),
        ('M.A','M.A'),
        ('Phd','Phd'),
        ('Diploma','Diploma'),
        ('HighSchool','HighSchool'),
        ('Intermediate','Intermediate'),

    ]
    profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE ,null=True)
    degree = models.CharField(max_length=100,choices=degree)
    college = models.CharField(max_length=100)
    board_or_university = models.CharField(max_length=100)
    passing_year = models.CharField(max_length=100)
    percentage = models.CharField(max_length=100)

    def __str__(self):
        return self.profile.user.name+" "+self.degree
   
class Skill(models.Model):
    skills_level=[
        ('basic','basic'),
        ('moderate','moderate'),
        ('advanced','advanced'),
    ]
    profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE ,null=True,related_name='skills')
    name = models.CharField(max_length=100)
   

    def __str__(self):
        return self.profile.user.name +'  have '+self.name
    


class Project(models.Model):
    profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="Describe your project")
    start_date = models.DateField()
    currently_working = models.BooleanField(default=False)
    end_date = models.DateField()
    Gitlink= models.CharField(max_length=100)
    link = models.CharField(max_length=100,help_text="Put yur web  hosting link here")

    def __str__(self):
        return self.profile.user.name+"  by  "+self.name 
    
class Apply(models.Model):
    status=[
        ('Resume Sent','Resume Sent'),
        ('Resume Viewed','Resume viewed'),
        ('Not selected','Not selected'),
        ('In Process','In Process'),
        ('Hired','Hired'),
        ('Resume Shortlisted','Resume Shortlisted')
    ]
    id=models.AutoField(primary_key=True)
    candidate_detail = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE,null=True,related_name='candidate_detail')
    recruiter_detail = models.ForeignKey(Recruiter, on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    about = models.TextField(help_text="Why should we hire you")
    applied_on = models.DateTimeField(auto_now_add=True)
    job_status=models.CharField(max_length=100,choices=status,default='Resume Sent')



    def __str__(self):
        return self.candidate_detail.user.name+" applied for "+self.recruiter_detail.company_name+" "+"for the post"+" "+self.job.title
    

class addLink(models.Model):
    link_option=[
        ('Github','Github'),
        ('LinkedIn','LinkedIn'),
        ('Twitter','Twitter'),
        ('Facebook','Facebook'),
        ('Instagram','Instagram'),
        ('Geeks For Geeks','Geeks For Geeks'),
        ('Hackerrank','Hackerrank'),
        ('Hackerearth','Hackerearth'),
        ('Codechef','Codechef'),
        ('Codeforces','Codeforces'),
        ('Leetcode','Leetcode'),
        ('Dev.to','Dev.to'),
        ('Medium','Medium'),
        ('Stackoverflow','Stackoverflow'),
        ('Other','Other'),


    ]
    profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=100,choices=link_option)
    link = models.CharField(max_length=100,help_text="Put yur  link here")

    def __str__(self):
        return self.profile.user.name+"  by  "+self.link
    

class Experience (models.Model):
    userprofile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE ,null=True,related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    currently_working = models.BooleanField(default=False)
    end_date = models.DateField()

    def __str__(self):
        return self.userprofile.user.name+"  by  "+self.company

class achievement(models.Model):
    userprofile=models.ForeignKey(ApplicantProfile,on_delete=models.CASCADE,null=True,related_name='achievement')
    text=models.TextField()
    date=models.DateField()
    Institution=models.CharField(max_length=40,null=True)

    def  __str__(self):
        
          return self.userprofile.user.name+" has "+self.text


class Message(models.Model):
    id=models.AutoField(primary_key=True)
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    subject=models.CharField(max_length=100)
    is_read=models.BooleanField(default=False)
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.name+" send message to "+self.receiver.name
    
    class Meta:
        ordering=['is_read','-timestamp']

class SaveJob(models.Model):
    id=models.AutoField(primary_key=True)
    candidate_detail = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE,null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_detail.user.name+" saved "+self.job.title
    


