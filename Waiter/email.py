from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.conf import settings

def send_feedback_email(email,name):
    context = {
        'name':name
    }

    html_body = render_to_string("emailMessage.html", context)

    message = EmailMultiAlternatives(
       subject='Thank you for the message',
       body="mail testing",
       from_email="no-reply <lucayanwork@gmail.com>",
       to=[email]
    )
    message.attach_alternative(html_body, "text/html")

    return message.send(fail_silently=False)


def send_to_me(email,subject, message,name):
    context = {
        'name' : name,
        'email' : email,
        'message': message,
    }
    email_body = render_to_string('emailMessage.txt',context)
    
    return send_mail(
        subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        ['info@italiantrufflerestaurant.co.uk'],
    )