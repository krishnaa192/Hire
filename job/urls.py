
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='home'),
    path('profile',views.profile,name='profile'),
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', views.candidate_signup, name='signup'),
    path('login/', views.candidate_login, name='login'),
    path('jobs', views.job_list, name='jobs'),
    path('logout/', views.logoutUser, name='logout'),
    path('candidate_profile/', views.candidate_profile, name='candidate_profile'),
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile'),
    path('recruiter_home/', views.recruiter_home, name='recruiter_home'),
    path('job_detail/<str:pk>/', views.job_detail, name='job_detail'),
    path('apply_job/<str:pk>/', views.apply_job, name='apply_job'),
    path('verify/', views.verifications_job, name='verifications_job'),
    path('about/', views.about, name='about'),
    path('k/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('user/', views.user_profile, name='user_profile'),
    path('job_create/', views.job_create, name='job_create'),
    path('setting', views.update_profile, name='setting'),
    path('applicant_profile', views.applicant_profile, name='applicant_profile'),
    path('updateApplicant', views.update_applicant_profile, name='updateApplicant'),
    path('add_education', views.education, name='add_education'),
    path('update_education/<int:pk>/', views.update_education, name='update_education'),
    path('add_project', views.project, name='add_project'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)