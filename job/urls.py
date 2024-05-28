
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('header/', views.header, name='header'),
    path('home', views.home, name='home'),
    path('profile/',views.profile,name='profile'),
    path('', views.welcome, name='welcome'),
    path('signup/', views.candidate_signup, name='signup'),
    path('login/', views.candidate_login, name='login'),
    path('jobs/', views.job_list, name='jobs'),
    path('logout/', views.logoutUser, name='logout'),

    # path('save_job/<str:pk>/', views.save_job, name='save_job'),
    
   
    path('job_detail/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply_job/<str:pk>/', views.apply_job, name='apply_job'),
    path('about/', views.about, name='about'),
    path('user/', views.user_profile, name='user_profile'),
    path('user/delete_education/<int:pk>/', views.delete_education, name='delete_education'),
    path('user/delete_project/<int:pk>/', views.delete_project, name='delete_project'),
    path('setting', views.update_profile, name='setting'),
    path('applicant_profile', views.applicant_profile, name='applicant_profile'),
    path('update', views.update_applicant_profile, name='updateApplicant'),
    path('add_education', views.education, name='add_education'),
    path('update_education/<int:pk>/', views.update_education, name='update_education'),
    path('add_project', views.project, name='add_project'),
    path('add-achievement',views.add_achievement,name='add_achievement'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),
    path('user/skill', views.add_skill, name='add_skill'),
    path('user/delete_skill/<int:pk>/', views.delete_skill, name='delete_skill'),
    path('links/', views.addlink, name='add_link'),

    path('deleteLink/<int:pk>/', views.deleteLink, name='delete_link'),
    #category endpoints
    path('jobs/category/<str:cat>/', views.category, name='web_dev'),
    path('job/application/<int:id>/',views.see_application ,name='see-application'),
    path('save_job/<int:pk>/', views.save_job, name='save_job'),
    path('saved_jobs/', views.saved_job, name='saved_jobs'),

]
