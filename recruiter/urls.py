from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.recruiter_home, name='recruiter_home'),
    path('k/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('list/<int:id>/', views.candidate_list, name='candidate_list'),
    path('job/', views.rec_job, name='job'),
    path('rec_header/', views.rec_header, name='rec_header'),
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile'),
    path('job_create/', views.job_create, name='job_create'),
    path('job_detail/<int:id>/', views.job_detail, name='job-detail'),
    path('job_list/', views.rec_job_list, name='job-list'),
    path('profile/<str:username>/', views.profile, name="rec_profile"),
    path('candidate_profile/<str:username>/', views.candidate_profile, name='candidate_profile'),
    path('send-email/',views.send_email,name='send_email'),

    
]
