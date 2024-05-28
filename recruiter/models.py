from job.models import *











class Recruiter_contacts(models.Model):
#social media choices
    social_media_choices=[
        ('linkedin','linkedin'),
        ('instagram','instagram'),
        ('facebook','facebook'),
        ('twitter','twitter'),
        ('Github','Github'),
        ('others','others'),
         
    ]
    recruiter=models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    social_media=models.CharField(max_length=100,choices=social_media_choices)
    link=models.URLField()

 
    def __str__(self):
        return self.social_media
    

class Recruitering_Manager(models.Model):
    recruiter=models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    location=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    linkedin=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

