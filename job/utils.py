# utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

def filter_and_sort_jobs(request, jobs):
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

    location_filter = request.GET.get('location')
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    return jobs


def send_job_application_notification(job_title, candidate_name, candidate_email):
    subject = 'Job Application'
    message = f'A new application has been submitted for the job "{job_title}" by {candidate_name}.'
    from_email = settings.DEFAULT_FROM_EMAIL  # You can set your default 'from' email in Django settings
    recipient_list = [candidate_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)