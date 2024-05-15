# Import the necessary modules
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

# Define the constant username
CONSTANT_USERNAME = "John Doe"  # Replace "John Doe" with the desired constant username

# Define the view function to send email
def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Assuming you're sending email as a POST parameter
        
        if email:
            # Long message content with constant username
            message = (
                f"Dear {CONSTANT_USERNAME},\n\n"
                "Congratulations! We are pleased to inform you that you have been shortlisted for further evaluation.\n\n"
                "Please find attached the details of the next steps in the selection process.\n\n"
                "Best regards,\n"
                "Your Company"
            )
            
            # Send the email
            send_mail('Congratulations! You have been shortlisted', message, settings.EMAIL_HOST_USER, [email])
            
            return HttpResponse('Email sent successfully!')
        else:
            return HttpResponse('Email address not provided')
    else:
        return HttpResponse('Invalid request method')
