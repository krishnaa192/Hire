from django.shortcuts import redirect
#import messages
from django.contrib import messages

def is_recruiter(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is a recruiter
        if request.user.is_authenticated and request.user.profile.is_recruiter:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a specific page if the user is not a recruiter
            return redirect('home' )  # Adjust the URL name accordingly
    return wrapped_view

def is_applicant(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is a applicant
        if request.user.is_authenticated and request.user.profile.is_applicant:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a specific page if the user is not a applicant
            return redirect('home')
    return wrapped_view
